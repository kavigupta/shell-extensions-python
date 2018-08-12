"""
Various functions to help run shell commands.
"""

from abc import ABCMeta, abstractmethod
from enum import Enum

import subprocess
import os

from .colors import PrintColors
from .path_manipulation import expand_user
from .tcombinator import TCombinator

def iterable(value):
    """
    Returns True iff the given value is iterable
    """
    try:
        iter(value)
        return True
    except: # pylint: disable=bare-except
        return False

class ProcessFailedException(RuntimeError):
    """
    An exception representing a failed process
    """
    pass

class ShellResult:
    """
    Represents the result of calling a shell program
    """
    def __init__(self, stdout, stderr, returncode):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode
    def __bool__(self):
        return self.returncode == 0
    def __repr__(self):
        return ""
    @staticmethod
    def _process(raw, single_line, as_lines):
        result = raw.decode('utf-8')
        if single_line:
            lines = [x for x in result.split(os.linesep) if x]
            if len(lines) != 1:
                raise RuntimeError("Not exactly one line: %s" % lines)
            result = lines[0]
        elif as_lines:
            result = result.split(os.linesep)
            if result[-1] == "":
                result.pop()
        return result
    def stdout(self, single_line=False, as_lines=False):
        """
        Output the stdout as a string with possible modifications
            single_line: strip away all leading and trailing whitespace, and error if there is more than one line
            as_lines: return a list of lines.
        """
        return self._process(self._stdout, single_line=single_line, as_lines=as_lines)

    def or_throw(self, throw=True): # pylint: disable=R1710
        """
        Throws if throw is truthy, and the return code was failure.

        You can set throw to be an exception to throw it
        """
        if self:
            return self # not an error
        if not throw:
            return self
        if throw is True:
            raise ProcessFailedException
        raise throw # pylint: disable=E0702

class FD(Enum):
    """
    File descriptors, either stdout or stderr
    """
    stdout = 1
    stderr = 2

def parse_command(command, print_direct):
    """
    Parses the given into a subprocess call.
    """
    pipe = None if print_direct else subprocess.PIPE
    if isinstance(command, str):
        return subprocess.Popen(command, shell=True, stdout=pipe, stderr=pipe)
    elif iterable(command):
        command = list(command)
        if all(isinstance(x, str) for x in command):
            return subprocess.Popen(command, stdout=pipe, stderr=pipe)
        else:
            raise RuntimeError("Cannot run %s: it has non-string elements" % command)
    else:
        raise RuntimeError("Expected str or some iterable, but got %s" % type(command))

class Process:
    """
    Represents a process, which can be iterated through and has several methods
    """
    def __init__(self, proc, print_direct):
        self.proc = proc
        self._exitcode = None
        self.print_direct = print_direct
    def __iter__(self):
        if not self.print_direct:
            yield from TCombinator(
                ((FD.stdout, line) for line in self.proc.stdout),
                ((FD.stderr, line) for line in self.proc.stderr)
            )
            self.proc.stdout.close()
            self.proc.stderr.close()
        self._exitcode = self.proc.wait()
    @property
    def exitcode(self):
        """
        Get the exit code for the underlying process. Throws an error if the process isn't complete
        """
        if self._exitcode is not None:
            return self._exitcode
        raise RuntimeError("No exit code for the current process")
    def collect(self, consumer_type):
        """
        Runs the given shell consumer on the contents of this process, then returns the exit code
        """
        if consumer_type is None:
            list(self)
            return ShellResult(b"", b"", self.exitcode)
        consumer = consumer_type()
        for fd, line in self:
            consumer.consume(fd, line)
        return ShellResult(consumer.stdout(), consumer.stderr(), self.exitcode)
    def __gt__(self, other):
        return self.collect(other)

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

class StderrRed(Consumer):
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

def r(command, mode=None, throw=False):
    """
    Run the given command, and optionally gather the stdout and stderr
        mode=Collect to gather, mode=StderrRed to print normal/red for stdout/stderr

    If throw is true, this raises a RuntimeError whenever the result has a nonzero exit code
    """
    return s(command, print_direct=mode is None).collect(mode).or_throw(throw)

def s(command, print_direct=False):
    """
    Run the given command, and optionally gather the stdout and stderr

    If throw is true, this raises a RuntimeError whenever the result has a nonzero exit code
    """
    return Process(parse_command(command, print_direct), print_direct)

def less(path):
    """
    Runs the linux command less on a file
    """
    return r(['less', expand_user(path)])

def cp(src, dest):
    """
    Runs the linux command cp on a file
    """
    return r(['cp', expand_user(src), expand_user(dest)])
