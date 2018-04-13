"""
Basic shell types
"""

import os
import os.path

class shell_str(str):
    """
    A wrapper around str with a few additional properties
    """
    def lines(self):
        """
        Converts a file into a list of lines
        """
        return shell_list(self.split(os.linesep))
    def dirname(self):
        """
        Gets the directory name of the given path
        """
        return shell_str(os.path.dirname(self))
    def basename(self):
        """
        Gets the file name of the given path
        """
        return shell_str(os.path.basename(self))

class shell_list(list):
    """
    A wrapper around list that provides a few additional properties
    """
    def unlines(self):
        """
        Converts to a single file with the given unlines
        """
        return shell_str(os.linesep.join(self) + os.linesep)
