"""
Tools for mapping over pipelines
"""

from abc import ABCMeta, abstractmethod

from .fd import FD

class PipelineMap(metaclass=ABCMeta):
    """
    A map over a pipeline's stdout/stderr stream
    """
    @abstractmethod
    def map(self, pipeline_stream):
        """
        Map over pipeline streams
        """
        pass

class LineMap(PipelineMap):
    """
    Represents a mapping over individual lines
        fds: which file descriptors to consider
    """
    def __init__(self, func, fds):
        self.__func = func
        self.__fds = fds
    def map(self, pipeline_stream):
        for fd, line in pipeline_stream:
            if fd in self.__fds:
                yield fd, self.__func(line)
            else:
                yield fd, line

class _Sort(PipelineMap):
    def map(self, pipeline_stream):
        stdouts = []
        for fd, line in pipeline_stream:
            if fd == FD.stdout:
                stdouts.append(line)
            else:
                yield fd, line
        for line in sorted(stdouts):
            yield FD.stdout, line

sort = _Sort() # pylint: disable=C0103
