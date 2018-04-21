"""
Implements basic unix uitilities.
"""

import os
import os.path

import shutil
import errno
import getpass

import glob as pyglob

from .shell_types import ShellStr, ShellList
from .path_manipulation import expand_user
from .interactive import ask_question, DisplayPath

def ls(path='.', sort_key=lambda x: x, a=True, full=False):
    """
    Returns a listing of the given path, sorted by name by default

    path: the directory to list the contents of
    sort_key: the key by which to sort the results, or None if you don't want the results sorted.
    """
    path = expand_user(path)
    result = os.listdir(path)
    result = [DisplayPath(spath, context=path) for spath in result]
    if sort_key is not None:
        result.sort(key=sort_key)
    if not a:
        result = [x for x in result if x[0] != '.']
    if full:
        result = [os.path.join(path, x) for x in result]
    return ShellList(result)

def cat(filename, mode=''):
    """
    Loads the given file as a ShellStr.
    """
    assert 'w' not in mode
    with open(expand_user(filename), mode + 'r') as f:
        return ShellStr(f.read())

def write(filename, contents, clobber=False, append=False):
    """
    Write the contents to the given file
    """
    if clobber and append:
        raise RuntimeError("clobbering and appending are mutually exclusive")
    elif clobber:
        mode = 'w'
    elif append:
        mode = 'a'
    else:
        mode = 'x'
    with open(filename, mode) as f:
        f.write(contents)

def pwd():
    """
    Get the present working directory as a ShellStr
    """
    return ShellStr(os.getcwd())

def rm(path, ignore_missing=False, recursively=False, interactive=True):
    """
    Removes the given normal file or empty folder.

    ignore_missing: do not error if the file does not exist
    recursively: remove a directory recursively if it contains values
    interactive: prompt rather than erroring if you encounter a file you are not allowed to delete
    """
    path = expand_user(path)
    if not os.path.exists(path):
        if ignore_missing:
            return
        else:
            raise RuntimeError("The file %s cannot be removed as it does not exist" % path)
    elif os.path.isdir(path):
        if ls(path) == []:
            os.rmdir(path)
        elif recursively:
            shutil.rmtree(path)
        elif interactive:
            if ask_question("Are you sure you want to remove %s: it is a directory with contents [yN]: " % path) == 'y':
                shutil.rmtree(path)
        else:
            raise RuntimeError("Cannot remove directory %s, it has contents" % path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        raise RuntimeError("The path %s represents an existing file that is not a directory or normal file" % path)


def mkdir(folder, error_if_exists=False):
    """
    Makes the given directory, returns False if the directory already exists.
        Alternatively, can error if the directory exists if error_if_exists is
        set to True.

    Errors if a file exists in place of the directory.
    """
    try:
        os.makedirs(folder)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(folder) and not error_if_exists:
            return False
        else:
            raise
    return True


def cd(path='~'):
    """
    Change the current directory to the given one.
    """
    if isinstance(path, str):
        path = os.path.abspath(expand_user(path))
        os.chdir(path)
        cd.stack.append(path)
        assert(path == pwd()), "cd failed"
    elif isinstance(path, int):
        if path < 1:
            raise RuntimeError("path should be a number > 1")
        path = -path - 1 # pylint: disable=E1130
        path_str = cd.stack[path]
        cd.stack = cd.stack[:path]
        cd(path_str)
    else:
        raise TypeError("path should either be int or str but was %s" % type(path))

cd.stack = []

def globs(glob_str):
    """
    Returns all the possible glob expansions of the given string
    """
    return pyglob.glob(glob_str)

def glob(glob_str):
    """
    Returns one glob expansion of the given string. If no match is found or multiple matches are found, it should crash.
    """
    results = globs(glob_str)
    if not results:
        raise RuntimeError("No matches for %s" % glob_str)
    elif len(results) > 1:
        raise RuntimeError("Multiple matches for %s: %s matches found" % (glob_str, len(results)))
    else:
        return results[0]

def whoami():
    """
    Get the current user
    """
    return getpass.getuser()
