"""
File descriptors, either stdout or stderr
"""

from enum import Enum

class FD(Enum):
    """
    File descriptors, either stdout or stderr
    """
    stdout = 1
    stderr = 2
