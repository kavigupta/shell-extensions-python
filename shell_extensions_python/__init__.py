"""
A package that is supposed to allow you to use python rather than bash as your shell.
"""

import shell_extensions_python.git as git

from .basic_shell_programs import ls, cat, pwd, cd, globs, glob, mkdir, write, rm, whoami
from .run_shell_commands import r, less, cp
from .shell_pickles import pload, ploads, psaves, psave
