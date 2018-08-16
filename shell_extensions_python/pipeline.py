"""
Pipelines are iterables with an interleaved standard out and standard error, which support
    operations such as piping into a collector and mapping
"""

from abc import ABCMeta, abstractmethod
from .pipeline_result import PipelineResult
from .pipeline_map import PipelineMap, LineMap
from .fd import FD

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
            return PipelineResult([], [], self.exitcode)
        consumer = consumer_type()
        for fd, line in self:
            consumer.consume(fd, line)
        return PipelineResult(consumer.stdout(), consumer.stderr(), self.exitcode)
    def __or__(self, mapper):
        """
        Maps the given mapper over this pipeline.
            If mapper is just a function, use a line mapping over stdout
        """
        return self._map(mapper, {FD.stdout})
    def __truediv__(self, mapper):
        """
        Maps the given mapper over this pipeline.
            If mapper is just a function, use a line mapping over stderr
        """
        return self._map(mapper, {FD.stderr})
    def __mod__(self, mapper):
        """
        Maps the given mapper over this pipeline.
            If mapper is just a function, use a line mapping over both stdout and stderr
        """
        return self._map(mapper, {FD.stdout, FD.stderr})
    def _map(self, mapper, fds):
        """
        Map the given mapper over this pipeline. If the mapper is just a function, map over fds
        """
        if isinstance(mapper, PipelineMap):
            return MappedPipeline(self, mapper)
        elif isinstance(mapper, type) and issubclass(mapper, PipelineMap):
            return MappedPipeline(self, mapper(fds))
        elif callable(mapper):
            return MappedPipeline(self, LineMap(mapper, fds))
        else:
            raise RuntimeError("Invalid mapping object, should be a "
                               + "PipelineMap or callable but was %s" % type(mapper))

class MappedPipeline(Pipeline):
    """
    Represents the result of a map operation
    """
    def __init__(self, pipeline, mapper):
        super().__init__()
        self.__pipeline = pipeline
        self.__mapper = mapper
    def _lines(self):
        # pylint: disable=W0212
        yield from self.__mapper.map(self.__pipeline._lines())
    def _end(self):
        # pylint: disable=W0212
        return self.__pipeline._end()
