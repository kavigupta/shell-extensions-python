"""
Pipelines are iterables with an interleaved standard out and standard error, which support
    operations such as piping into a collector and mapping
"""
# TODO add mapping


from abc import ABCMeta, abstractmethod
from enum import Enum
from .pipeline_result import PipelineResult

class FD(Enum):
    """
    File descriptors, either stdout or stderr
    """
    stdout = 1
    stderr = 2

class Pipeline(metaclass=ABCMeta):
    """
    Represents an iterable with a standard output and error that both occur in time,
        as well as an exit code that is only valid once the iteration is complete.
    """
    def __init__(self):
        self._exitcode = None
    @abstractmethod
    def _lines(self):
        """
        Yields several (FD, str) representing lines and the file descriptors they
            find themselves on
        """
        pass
    @abstractmethod
    def _end(self):
        """
        Ends the pipeline, performing cleanup, and returing an exit code.
            This uses unix conventions, 0 for success, anything else is failure

        Only to be called once _lines is exhausted
        """
        pass
    def __iter__(self):
        yield from self._lines()
        self._exitcode = self._end()
    @property
    def exitcode(self):
        """
        Get the exit code for the underlying process. Throws an error if the process isn't complete
        """
        if self._exitcode is not None:
            return self._exitcode
        raise RuntimeError("No exit code for the current process")
    def __gt__(self, consumer_type):
        """
        Runs the given shell consumer on the contents of this process, then returns the exit code
        """
        if consumer_type is None:
            list(self)
            return PipelineResult(b"", b"", self.exitcode)
        consumer = consumer_type()
        for fd, line in self:
            consumer.consume(fd, line)
        return PipelineResult(consumer.stdout(), consumer.stderr(), self.exitcode)
