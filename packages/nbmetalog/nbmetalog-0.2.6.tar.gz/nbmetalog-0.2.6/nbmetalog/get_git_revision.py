from functools import lru_cache
import pathlib
import subprocess

from . import _except_return_none
from . import get_notebook_path

@lru_cache()
@_except_return_none
def get_git_revision():
    return subprocess.check_output([
        'git',
        '-C',
        get_notebook_path(),
        'rev-parse',
        '--short',
        'HEAD',
    ]).decode('ascii').strip()
