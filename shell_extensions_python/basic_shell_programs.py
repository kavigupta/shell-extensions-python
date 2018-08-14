"""
Implements basic unix uitilities.
"""

import os
import os.path

import shutil
import errno
import getpass

import glob as pyglob

from .autorun import autorun
from .shell_types import ShellStr, ShellList, ShellBool
from .path_manipulation import expand_user
from .interactive import Interactive, DisplayPath

@autorun
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
        raise ValueError("clobbering and appending are mutually exclusive")
    elif clobber:
        mode = 'w'
    elif append:
        mode = 'a'
    else:
        mode = 'x'
    with open(filename, mode) as f:
        f.write(contents)
    return ShellBool.true

@autorun
def pwd():
    """
    Get the present working directory as a ShellStr
    """
    return ShellStr(os.getcwd())

class CannotRemoveDirectoryError(OSError):
    """
    Represents an error involving incorrectly removing a directory
    """
    def __init__(self, path):
        super().__init__("Cannot remove directory %s, it has contents" % path)

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
            return ShellBool.true
        else:
            raise FileNotFoundError("The file %s cannot be removed as it does not exist" % path)
    elif os.path.isdir(path):
        if ls(path) == []:
            os.rmdir(path)
            return ShellBool.true
        elif recursively:
            shutil.rmtree(path)
            return ShellBool.true
        elif interactive:
            if Interactive.ask_question(("Are you sure you want to remove %s:" \
                    + " it is a directory with contents [yN]: ") % path) == 'y':
                shutil.rmtree(path)
                return ShellBool.true
            return ShellBool.false
        else:
            raise CannotRemoveDirectoryError(path)
    elif os.path.isfile(path):
        os.remove(path)
        return ShellBool.true
    else:
        raise RuntimeError("The path %s represents an existing file that is not a directory or normal file" % path)

def mv(src, dst, overwrite=False, create_dir=True):
    """
    Moves the file `src` to have the name `dst`. If you want to move `src` into a folder use `move_to`.
        overwrite=False:    if `overwrite` is False, will not clobber a file if it exists at `dst`
        create_dir=True:    if `create_dir` is True, creates all directories above `dst` if necessary
    """
    src = os.path.abspath(expand_user(src))
    dst = os.path.abspath(expand_user(dst))
    if os.path.isdir(dst):
        raise RuntimeError("Destination file %s exists and is a directory: you probably want `move_to`" % dst)
    if os.path.exists(dst) and not overwrite:
        raise RuntimeError("Destination file %s exists" % dst)
    folder = os.path.dirname(dst)
    if not os.path.exists(folder):
        if create_dir:
            mkdir(folder)
        else:
            raise RuntimeError("Destination folder %s does not exist" % folder)
    shutil.move(src, dst)
    return ShellBool.true


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
            return ShellBool.false
        else:
            raise
    return ShellBool.true

@autorun
def cd(path='~'):
    """
    Change the current directory to the given one.
    """
    if isinstance(path, str):
        path = os.path.realpath(expand_user(path))
        os.chdir(path)
        cd.stack.append(path)
        assert(path == pwd()), "cd failed"
        return ShellBool.true
    elif isinstance(path, int):
        if path < 1:
            raise RuntimeError("path should be a number > 1")
        path = -path - 1 # pylint: disable=E1130
        path_str = cd.stack[path]
        cd.stack = cd.stack[:path]
        cd(path_str)
        return ShellBool.true
    else:
        raise TypeError("path should either be int or str but was %s" % type(path))

cd.stack = []

def globs(glob_str):
    """
    Returns all the possible glob expansions of the given string
    """
    return pyglob.glob(expand_user(glob_str))

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

@autorun
def whoami():
    """
    Get the current user
    """
    return getpass.getuser()
