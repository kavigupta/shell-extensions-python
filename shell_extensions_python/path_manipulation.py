"""
Tools for manipulating paths
"""

import os.path

def expand_user(path):
    """
    Like expanduser
    """
    return os.path.expanduser(path)

def unexpand_user(path):
    """
    Undoes expand_user
    """
    home = expand_user('~')
    if path.startswith(home):
        path = "~" + path[len(home):]
    return path

def basename(path):
    """
    Get the filename of the given path
    """
    return os.path.basename(path)

def dirname(path):
    """
    Get the directory of the given path
    """
    return os.path.dirname(path)

def join(path, name):
    """
    Return $path/$name
    """
    return os.path.join(path, name)
