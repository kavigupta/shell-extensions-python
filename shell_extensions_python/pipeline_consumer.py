"""
Classes for consuming pipelines, and then returning the standard out and standard error.
"""

from abc import ABCMeta, abstractmethod

from .colors import PrintColors
from .pipeline import FD

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
        if fd == FD.stdout:
            print(line.decode('utf-8'), end="")
        elif fd == FD.stderr:
            print(PrintColors.red + line.decode('utf-8') + PrintColors.reset, end="")
    @staticmethod
    def stdout():
        return b""
    @staticmethod
    def stderr():
        return b""

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
        return b"".join(self.stdouts)
    def stderr(self):
        return b"".join(self.stderrs)
