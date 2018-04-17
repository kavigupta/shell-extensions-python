
import os
from enum import Enum
from colorama import Fore, Style

def ask_question(prompt):
    return input(prompt)

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
