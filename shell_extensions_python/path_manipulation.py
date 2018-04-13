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
