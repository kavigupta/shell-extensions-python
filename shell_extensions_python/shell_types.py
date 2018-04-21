"""
Basic shell types
"""

import os
import os.path

from enum import Enum

class ShellStr(str):
    """
    A wrapper around str with a few additional properties
    """
    def lines(self):
        """
        Converts a file into a list of lines
        """
        return ShellList(self.split(os.linesep))
    def dirname(self):
        """
        Gets the directory name of the given path
        """
        return ShellStr(os.path.dirname(self))
    def basename(self):
        """
        Gets the file name of the given path
        """
        return ShellStr(os.path.basename(self))

class ShellList(list):
    """
    A wrapper around list that provides a few additional properties
    """
    def unlines(self):
        """
        Converts to a single file with the given unlines
        """
        return ShellStr(os.linesep.join(self) + os.linesep)

class ShellBool(Enum):
    true = True
    false = False
    def __bool__(self):
        return self.value
    def __repr__(self):
        return ""
