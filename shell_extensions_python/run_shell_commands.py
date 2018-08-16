"""
Various functions to help run shell commands.
"""

from abc import ABCMeta, abstractmethod


import subprocess

from .pipeline import FD, Pipeline
from .colors import PrintColors
from .path_manipulation import expand_user
from .tcombinator import TCombinator

class ProcessFailedException(RuntimeError):
    """
    An exception representing a failed process
    """
    pass

class Process(Pipeline):
    """
    Represents a process, which can be iterated through and has several methods
    """
    def __init__(self, proc, print_direct):
        super().__init__()
        self.proc = proc
        self.print_direct = print_direct
    def _lines(self):
        if not self.print_direct:
            yield from TCombinator(
                ((FD.stdout, line) for line in self.proc.stdout),
                ((FD.stderr, line) for line in self.proc.stderr)
            )
            self.proc.stdout.close()
            self.proc.stderr.close()
    def _end(self):
        return self.proc.wait()

class Consumer(metaclass=ABCMeta):
    """
    Represents a callback that can consume lines and optionally stores them
    """
    @abstractmethod
    def consume(self, fd, line):
        """
        Consume the given line on the given descriptor
        """
    @abstractmethod
    def stdout(self):
        """
        Returns the stdout seen
        """
    @abstractmethod
    def stderr(self):
        """
        Returns the stderr seen
        """

class StderrRed(Consumer): # pragma: no cover
    """
    Prints standard out and standard error to the screen.
    """
    @staticmethod
    def consume(fd, line):
        if fd == FD.stdout:
            print(line.decode('utf-8'), end="")
        elif fd == FD.stderr:
            print(PrintColors.red + line.decode('utf-8') + PrintColors.reset, end="")
    @staticmethod
    def stdout():
        return b""
    @staticmethod
    def stderr():
        return b""

class Collect(Consumer):
    """
    Collects standard out and standard error in memory
    """
    def __init__(self):
        self.stdouts = []
        self.stderrs = []
    def consume(self, fd, line):
        {FD.stdout : self.stdouts, FD.stderr : self.stderrs}[fd].append(line)
    def stdout(self):
        return b"".join(self.stdouts)
    def stderr(self):
        return b"".join(self.stderrs)

def re(*command, mode=None):
    """
    Run the given command, and optionally gather the stdout and stderr
        mode=Collect to gather, mode=StderrRed to print normal/red for stdout/stderr

    Does not do any shell expansion
    """
    return se(*command, print_direct=mode is None) > mode

def r(command, mode=None):
    """
    Like re, but does shell expansion on its string argument
    """
    return s(command, print_direct=mode is None) > mode

def se(*command, print_direct=False):
    """
    Run the given command, and allow ability to gather output

    Does not do any shell expansion
    """
    pipe = None if print_direct else subprocess.PIPE
    if not all(isinstance(x, str) for x in command):
        raise RuntimeError("Cannot run %s: it has non-string elements" % command)
    return Process(subprocess.Popen(command, stdout=pipe, stderr=pipe), print_direct)

def s(command, print_direct=False):
    """
    Like se, but does shell expansion on its string argument
    """
    pipe = None if print_direct else subprocess.PIPE
    if not isinstance(command, str):
        raise RuntimeError("command argument to s must be of type str but was %s" % type(command))
    return Process(subprocess.Popen(command, shell=True, stdout=pipe, stderr=pipe), print_direct)

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
