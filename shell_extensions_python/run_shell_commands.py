"""
Various functions to help run shell commands.
"""

import subprocess

def iterable(value):
    """
    Returns True iff the given value is iterable
    """
    try:
        iter(value)
        return True
    except: # pylint: disable=bare-except
        return False

def r(command, std=False, err=False):
    """
    Run the given command, and optionally gather the stdout and stderr

    If command is a string, run it as a shell command, if command is an iterable, run it as a execve command.
    """
    std_proc = subprocess.PIPE if std else None
    err_proc = subprocess.PIPE if err else None
    if isinstance(command, str):
        return subprocess.run(command, shell=True, stdout=std_proc, stderr=err_proc)
    elif iterable(command):
        command = list(command)
        if all(isinstance(x, str) for x in command):
            return subprocess.run(command, stdout=std_proc, stderr=err_proc)
    raise RuntimeError("Cannot run %s" % command)
