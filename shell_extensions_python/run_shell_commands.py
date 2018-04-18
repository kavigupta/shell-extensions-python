"""
Various functions to help run shell commands.
"""

import subprocess

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

def r(command, std=False, err=False, throw=False):
    """
    Run the given command, and optionally gather the stdout and stderr

    If command is a string, run it as a shell command, if command is an iterable, run it as a execve command.

    If throw is true, this raises a RuntimeError whenever the result has a nonzero exit code
    """
    if throw is True:
        throw = ProcessFailedException
    std_proc = subprocess.PIPE if std else None
    err_proc = subprocess.PIPE if err else None
    if isinstance(command, str):
        result = subprocess.run(command, shell=True, stdout=std_proc, stderr=err_proc)
    elif iterable(command):
        command = list(command)
        if all(isinstance(x, str) for x in command):
            result = subprocess.run(command, stdout=std_proc, stderr=err_proc)
        else:
            raise RuntimeError("Cannot run %s: it has non-string elements" % command)
    else:
        raise RuntimeError("Expected str or some iterable, but got %s" % type(command))
    if result.returncode != 0 and throw:
        raise throw("Bad exit code: %s" % result.returncode)
    return result

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
