from collections.abc import Callable, Iterable, MutableSequence, Sequence
import asyncio
from concurrent.futures import Executor, ThreadPoolExecutor
from functools import partial
import locale
import argparse
import re
from typing import Pattern
from contextlib import contextmanager, nullcontext
from shlex import quote
from fcntl import flock, LOCK_EX, LOCK_UN
from pathlib import Path
from subprocess import PIPE, DEVNULL, CalledProcessError
import sys
import logging
from typing import Any, TypeVar, cast
from os import cpu_count

logger = logging.getLogger(__name__)

Number = TypeVar('Number', int, float)

class PartitionHandler(logging.Handler):
    '''Give a handler that partitions to false if the predicate resolves False,
    and true if it resolves True.
    '''

    __slots__ = ('predicate', 'false', 'true')

    def __init__(self,
        predicate: Callable[[logging.LogRecord], bool],
        false: logging.Handler,
        true: logging.Handler
    ):
        super().__init__()

        self.predicate = predicate
        self.false = false
        self.true = true

    def emit(self, record: logging.LogRecord) -> None:
        if self.predicate(record):
            self.true.handle(record)
        else:
            self.true.handle(record)

    def setFormatter(self, fmt: logging.Formatter) -> None:
        super().setFormatter(fmt)
        self.true.setFormatter(fmt)
        self.false.setFormatter(fmt)

    def addFilter(self, filter: logging.Filter) -> None:
        super().addFilter(filter)
        self.true.addFilter(filter)
        self.false.addFilter(filter)

    def removeFilter(self, filter: logging.Filter) -> None:
        super().removeFilter(filter)
        self.true.removeFilter(filter)
        self.false.removeFilter(filter)

    def close(self) -> None:
        super().close()
        self.true.close()
        self.false.close()

def _is_record_stderr(record: logging.LogRecord) -> bool:
    return record.levelno > logging.INFO

def setup_logging(verbosity: int):
    rootlogger = logging.getLogger()
    level = logging.WARNING - (verbosity * 10)
    rootlogger.setLevel(level)
    rootlogger.handlers = [
        PartitionHandler(
            predicate=_is_record_stderr,
            false=logging.StreamHandler(sys.stdout),
            true=logging.StreamHandler(sys.stderr),
        )
    ]
    rootlogger.handlers[0].setFormatter(logging.Formatter('{levelname}: {message}', style='{'))

def convert_path(source: Path, basedir: Path, legal: Pattern, replace: str, output: Path, suffix: str):
    if not source.exists():
        raise RuntimeError('file must exist')

    if basedir not in source.parents:
        raise RuntimeError('file must be in basepath')

    relative_path = source.relative_to(basedir)
    filtered_relative_path: Path | None = None

    for part in relative_path.parts:
        filtered_part = ''
        for char in part:
            if legal.match(char):
                filtered_part += char
            else:
                filtered_part += replace.format(ord(char))

        if filtered_relative_path is None:
            filtered_relative_path = Path(filtered_part)
        else:
            filtered_relative_path /= filtered_part

    if filtered_relative_path is None:
        raise RuntimeError('Path was the same as the base dir')

    return output / filtered_relative_path.with_suffix(suffix)


async def convert(
    source: Path,
    output: Path,
    semaphore: asyncio.Semaphore | nullcontext[None],
    basedir: Path,
    legal: Pattern,
    replace: str,
    suffix: str,
    dry_run: bool,
    input_args: Iterable[str],
    output_args: Iterable[str],
    executor: Executor,
):
    async with semaphore:
        loop = asyncio.get_running_loop()

        source = source.resolve()

        destination = await loop.run_in_executor(executor, partial(convert_path,
            source=source,
            basedir=basedir,
            legal=legal,
            replace=replace,
            output=output,
            suffix=suffix,
        ))

        if destination.exists():
            logging.debug('Skipping existing %s', quote(str(destination)))
            return

        # Don't need special locking because this is asyncio.

        args = [
            'ffmpeg',
            *input_args,
            '-i', str(source),
            *output_args,
            '-n', str(destination),
        ]

        commandline = ' '.join(map(quote, args))
        logging.debug(commandline)

        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)

            logging.info('writing %s', quote(str(destination)))
            process = await asyncio.create_subprocess_exec(
                *args,
                stdin=DEVNULL,
                stdout=PIPE,
                stderr=PIPE,
            )

            stdout: bytes | str
            stderr: bytes | str

            stdout, stderr = await process.communicate()

            assert process.returncode is not None, 'returncode should always be set at this point'

            try:
                stdout = cast(bytes, stdout).decode('utf-8')
            except Exception:
                pass

            try:
                stderr = cast(bytes, stderr).decode('utf-8')
            except Exception:
                pass


            if process.returncode == 0:
                logging.info('wrote %s', quote(str(destination)))
            else:
                raise CalledProcessError(returncode=process.returncode, cmd=commandline, output=stdout, stderr=stderr)

async def amain() -> int:
    parser = argparse.ArgumentParser(description='Use ffmpeg to convert music into a destination, skipping existing files')
    parser.add_argument('-d', '--dry-run', action='store_true', help="Don't run ffmpeg")
    parser.add_argument('-q', '--quiet', action='count', help="decrease verbosity, specified up to 2 times.", default=0)
    parser.add_argument('-v', '--verbose', action='count', help="increase verbosity, specified up to 2 times.", default=0)
    parser.add_argument('-b', '--basedir', help='The base directory to consider file paths relative to.  Defaults to the current path.  This is used to build the output directory.  All inputs must be below this path.', type=Path, default=Path.cwd())
    parser.add_argument('-o', '--output', help='The destination directory. default: %(default)s.', type=Path, default=Path('.'))
    parser.add_argument('-l', '--legal', help='regex matching legal characters in output path and filenames, non-matching codepoints will be encoded. default: %(default)r', default='.')
    parser.add_argument('-r', '--replace', help='Replacement format string for replacing illegal characters, passed the codepoint, default: %(default)r', default='_{:X}_')
    parser.add_argument('-j', '--jobs', help='Parallel jobs, default to number of CPUs. 0 for unbounded.', type=int, default=cpu_count() or 1)
    parser.add_argument('-s', '--suffix', help='New suffix.  default: %(default)r', default='.opus')
    parser.add_argument('-I', '--input-arg', help='Add an ffmpeg input argument', action='append', default=[])
    parser.add_argument('-O', '--output-arg', help='Add an ffmpeg output argument', action='append', default=[])
    parser.add_argument('input', help='The input files', type=Path, nargs='+')
    args = parser.parse_args()

    input: Sequence[Path] = sorted(args.input)
    output: Path = args.output
    basedir: Path = args.basedir
    dry_run: bool = args.dry_run
    verbosity: int = args.verbose - args.quiet
    legal = re.compile(args.legal)
    replace: str = args.replace
    jobs: int = args.jobs
    suffix: str = args.suffix
    input_args: Sequence[str] = args.input_arg
    output_args: Sequence[str] = args.output_arg

    semaphore: asyncio.Semaphore | nullcontext[None]
    if jobs > 0:
        threads = jobs
        semaphore = asyncio.Semaphore(jobs)
    else:
        threads = cpu_count() or 1
        semaphore = nullcontext(None)

    setup_logging(verbosity)

    if not basedir.exists():
        logger.critical('basedir must exist')
        sys.exit(1)

    basedir = basedir.resolve()

    tasks: MutableSequence[asyncio.Task]  = []

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(threads) as executor:
        for source in input:
            tasks.append(asyncio.create_task(convert(
                source=source,
                output=output,
                semaphore=semaphore,
                basedir=basedir,
                legal=legal,
                replace=replace,
                suffix=suffix,
                dry_run=dry_run,
                input_args=input_args,
                output_args=output_args,
                executor=executor,
            )))

        exitcode = 0

        for task in tasks:
            try:
                await task
            except Exception as e:
                exitcode = 1
                logging.error('conversion failed: %s', e)
                logging.debug('conversion failed.', exc_info=e)
                if isinstance(e, CalledProcessError):
                    logging.info('stdout: %s', e.stdout)
                    logging.error('stderr: %s', e.stderr)

        return exitcode

def main() -> int:
    try:
        return asyncio.run(amain())
    except KeyboardInterrupt:
        logging.info('Aborted')
        return 1

if __name__ == '__main__':
    main()
