"""
Contains functions relevant to user interaction.
"""


import os
import sys
from enum import Enum
from colorama import Fore, Style

from .run_shell_commands import ShellResult
from .shell_types import ShellBool

class Interactive:
    """
    Ask the user a question
    """
    ask_question = input

class FileType(Enum):
    """
    Represents a file type, whose value is equal to the style that the path should be printed with
    """
    directory = Style.BRIGHT + Fore.BLUE
    executable = Style.BRIGHT + Fore.GREEN
    normal_file = Fore.WHITE
    missing = Fore.RED
    link = Style.BRIGHT + Fore.CYAN

    @staticmethod
    def classify(path):
        """
        Classifies the given path as one of the FileType values
        """
        if not os.path.exists(path):
            return FileType.missing
        if os.path.islink(path) or os.path.ismount(path):
            return FileType.link
        if os.path.isdir(path):
            return FileType.directory
        if os.access(path, os.X_OK):
            return FileType.executable
        return FileType.normal_file

class DisplayPath(str):
    """
    A display path, which is exactly like a string, except that it __repr__'s colored in.
    """
    def __new__(cls, path, context):
        result = str.__new__(cls, path)
        result.type = FileType.classify(os.path.join(context, path))
        return result
    def __repr__(self):
        return self.type.value + super().__repr__() + Style.RESET_ALL

def is_displayed(value):
    """
    Whether or not the given value should be displayed on the screen
    """
    return not isinstance(value, (ShellBool, ShellResult))

def modified_displayhook(value, original_displayhook=sys.displayhook):
    """
    Make sure that ShellBool results in no value
    """
    if not is_displayed(value):
        return None
    if hasattr(value, '__repr_proxy__'):
        return modified_displayhook(value.__repr_proxy__())
    return original_displayhook(value)
