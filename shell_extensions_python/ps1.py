"""
Several extensions for python to be usable as a bash-style shell.
"""

import sys

from .basic_shell_programs import pwd
from .path_manipulation import unexpand_user

class PS1:
    """
    A class representing the left prompt
    """
    def __str__(self):
        return unexpand_user(pwd()) + " $ "

    @staticmethod
    def set():
        """
        Set this as the PS1
        """
        sys.ps1 = PS1()
