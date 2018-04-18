"""
A package that is supposed to allow you to use python rather than bash as your shell.
"""

from .basic_shell_programs import ls, cat, pwd, cd, globs, glob, mkdir, write, rm
from .run_shell_commands import r
from .shell_pickles import pload, ploads, psaves, psave
from .ps1 import PS1
