"""
Classes for consuming pipelines, and then returning the standard out and standard error.
"""

from abc import ABCMeta, abstractmethod

from .colors import PrintColors
from .fd import FD
from .shell_types import decode_line

class PipelineConsumer(metaclass=ABCMeta):
    """
    Represents a callback that can consume lines and optionally stores them
    """
    @abstractmethod
    def consume(self, fd, line):
        """
        Consume the given line on the given descriptor
        """
    @abstractmethod
    def stdout(self):
        """
        Returns the stdout seen
        """
    @abstractmethod
    def stderr(self):
        """
        Returns the stderr seen
        """

class Terminal(PipelineConsumer): # pragma: no cover
    """
    Prints standard out and standard error to the screen.
    """
    @staticmethod
    def consume(fd, line):
        line = decode_line(line)
        if fd == FD.stdout:
            print(line, end="")
        elif fd == FD.stderr:
            print(PrintColors.red + line + PrintColors.reset, end="")
    @staticmethod
    def stdout():
        return []
    @staticmethod
    def stderr():
        return []

class Collect(PipelineConsumer):
    """
    Collects standard out and standard error in memory
    """
    def __init__(self):
        self.stdouts = []
        self.stderrs = []
    def consume(self, fd, line):
        {FD.stdout : self.stdouts, FD.stderr : self.stderrs}[fd].append(line)
    def stdout(self):
        return self.stdouts
    def stderr(self):
        return self.stderrs
