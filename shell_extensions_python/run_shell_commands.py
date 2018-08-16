"""
Various functions to help run shell commands.
"""

import subprocess

from .fd import FD
from .pipeline import Pipeline
from .path_manipulation import expand_user
from .tcombinator import TCombinator

class ProcessFailedException(RuntimeError):
    """
    An exception representing a failed process
    """
    pass

class Process(Pipeline):
    """
    A pipeline created by the standard out and error of a process
    """
    def __init__(self, proc, print_direct, raw_bytes):
        super().__init__()
        self.proc = proc
        self.print_direct = print_direct
        self.raw_bytes = raw_bytes
    def _lines(self):
        if not self.print_direct:
            yield from TCombinator(
                ((FD.stdout, self.__encode(line)) for line in self.proc.stdout),
                ((FD.stderr, self.__encode(line)) for line in self.proc.stderr)
            )
            self.proc.stdout.close()
            self.proc.stderr.close()
    def _end(self):
        return self.proc.wait()
    def __encode(self, line):
        if self.raw_bytes:
            return line
        return line.decode('utf-8')

class cat(Pipeline): # pylint: disable=C0103
    """
    A pipeline created by reading a file to stdout

    Return code 0 if successful, 1 if there was an error reading the file (e.g., not found)
        Acts like the unix utility cat
    """
    def __init__(self, filename, raw_bytes=False):
        super().__init__()
        try:
            self.__handle = open(filename, "r" + "b" * raw_bytes)
            self.__errors = []
            self.__exitcode = 0
        except IOError as e:
            self.__handle = None
            self.__errors = [str(e).encode('utf-8')]
            self.__exitcode = 1
    def _lines(self):
        if self.__handle is not None:
            for line in self.__handle:
                yield FD.stdout, line
        for error in self.__errors:
            yield FD.stderr, error
    def _end(self):
        if self.__handle is not None:
            self.__handle.close()
        return self.__exitcode

def re(*command, mode=None):
    """
    Run the given command, and optionally gather the stdout and stderr
        mode=Collect to gather, mode=Terminal to print normal/red for stdout/stderr

    Does not do any shell expansion
    """
    return se(*command, print_direct=mode is None) > mode

def r(command, mode=None):
    """
    Like re, but does shell expansion on its string argument
    """
    return s(command, print_direct=mode is None) > mode

def se(*command, print_direct=False, raw_bytes=False):
    """
    Run the given command, and allow ability to gather output

    Does not do any shell expansion
    """
    pipe = None if print_direct else subprocess.PIPE
    if not all(isinstance(x, str) for x in command):
        raise RuntimeError("Cannot run %s: it has non-string elements" % command)
    return Process(subprocess.Popen(command, stdout=pipe, stderr=pipe), print_direct, raw_bytes=raw_bytes)

def s(command, print_direct=False, raw_bytes=False):
    """
    Like se, but does shell expansion on its string argument
    """
    pipe = None if print_direct else subprocess.PIPE
    if not isinstance(command, str):
        raise RuntimeError("command argument to s must be of type str but was %s" % type(command))
    return Process(subprocess.Popen(command, shell=True, stdout=pipe, stderr=pipe), print_direct, raw_bytes=raw_bytes)

def throw(exc):
    """
    Raise the given error. To be used like
        r('make') or throw(RuntimeError("make failed"))
    """
    raise exc

def less(path): # pragma: no cover
    """
    Runs the linux command less on a file
    """
    return re('less', expand_user(path))

def cp(src, dest):
    """
    Runs the linux command cp on a file
    """
    return re('cp', expand_user(src), expand_user(dest))
