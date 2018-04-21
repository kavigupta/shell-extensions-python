"""
A package that is supposed to allow you to use python rather than bash as your shell.
"""

from . import git

from .basic_shell_programs import ls, cat, pwd, cd, globs, glob, mkdir, write, rm, whoami, CannotRemoveDirectoryError
from .run_shell_commands import r, less, cp
from .shell_pickles import pload, ploads, psaves, psave
