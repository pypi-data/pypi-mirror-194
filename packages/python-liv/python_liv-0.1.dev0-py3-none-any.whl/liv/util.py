import io
from contextlib import redirect_stdout
from os.path import realpath
from pathlib import Path
from typing import Optional

from coveriteam.util import set_cache_directories, set_cache_update


def capture_stdout(fun):
    with io.StringIO() as buf, redirect_stdout(buf):
        res = fun()
        return (res, buf.getvalue())


def setup_cache_handling(args):
    """
    Set up the caches respecting options provided via @args
    """
    cache_dir = _get_cache_dir(args)
    if cache_dir:
        set_cache_directories(d=cache_dir)


def _get_cache_dir(args) -> Optional[Path]:
    if args.cache_dir:
        return Path(args.cache_dir)
    # if there is a local lib directory, we run a standalone version, so we use this
    file_path: Path = Path(realpath(__file__))
    lib_dir: Path = file_path.parent.parent.joinpath("lib", "cvt_cache")
    if lib_dir.is_dir():
        return lib_dir
