"""
Various functions to help run shell commands.
"""

from abc import ABCMeta, abstractmethod
from enum import Enum

import subprocess
import os
from threading import Thread

from .colors import PrintColors
from .path_manipulation import expand_user

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




def r(command, std=False, err=False, throw=False, callback=None):
    """
    Run the given command, and optionally gather the stdout and stderr

    If command is a string, run it as a shell command, if command is an iterable, run it as a execve command.

    If throw is true, this raises a RuntimeError whenever the result has a nonzero exit code
    """
    if throw is True:
        throw = ProcessFailedException
    stdout_buf = Buffer.create(std)
    stderr_buf = Buffer.create(err)
    if callback is None:
        callback = DoNothingCallback() if std or err else ColorPrintCallback()
    if isinstance(command, str):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif iterable(command):
        command = list(command)
        if all(isinstance(x, str) for x in command):
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            raise RuntimeError("Cannot run %s: it has non-string elements" % command)
    else:
        raise RuntimeError("Expected str or some iterable, but got %s" % type(command))
    def stdout_thread():
        "A thread for stdout"
        for line in proc.stdout:
            stdout_buf.new_data(line)
            callback.callback(FD.stdout, line)
    stdout_thread = Thread(target=stdout_thread)
    def stderr_thread():
        "A thread for stderr"
        for line in proc.stderr:
            stderr_buf.new_data(line)
            callback.callback(FD.stderr, line)
    stderr_thread = Thread(target=stderr_thread)
    stdout_thread.start()
    stderr_thread.start()
    stdout_thread.join()
    stderr_thread.join()

    exitcode = proc.wait()
    proc.stdout.close()
    proc.stderr.close()
    if exitcode != 0 and throw:
        raise throw("Bad exit code: %s" % exitcode)
    return ShellResult(stdout_buf.contents(), stderr_buf.contents(), exitcode)

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
