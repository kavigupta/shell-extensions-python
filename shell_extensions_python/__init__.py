"""
A package that is supposed to allow you to use python rather than bash as your shell.
"""

from sys import argv

from tempfile import NamedTemporaryFile

from . import git

from .basic_shell_programs import ls, read, pwd, cd, globs, glob, mkdir, write, rm, mv, move_to, whoami, \
    symlink, CannotRemoveDirectoryError
from .run_shell_commands import r, re, s, throw, less, cp, ProcessFailedException, cat
from .pipeline_consumer import Terminal, Collect
from .shell_pickles import pload, ploads, psaves, psave
from .pipeline_map import sort, head, retain
from .grep import cgrep
from .fd import FD

from .colors import PrintColors
