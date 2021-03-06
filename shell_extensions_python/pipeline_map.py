"""
Tools for mapping over pipelines
"""

from abc import ABCMeta, abstractmethod

class PipelineMap(metaclass=ABCMeta):
    """
    A map over a pipeline's stdout/stderr stream
    """
    @abstractmethod
    def map(self, pipeline_stream): # pragma: no cover
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

def sort(key=lambda x: x):
    """
    Sorts the contents using the natural order specified by `key`
    """
    class _Sort(PipelineMap):
        def __init__(self, fds):
            self.__fds = fds
        def map(self, pipeline_stream):
            to_sort = []
            for fd, line in pipeline_stream:
                if fd in self.__fds:
                    to_sort.append((fd, line))
                else:
                    yield fd, line
            for fd, line in sorted(to_sort, key=lambda fd_line: key(fd_line[1])):
                yield fd, line
    return _Sort

def head(count):
    """
    Gets the first `count` elements from a stream
    """
    class _Head(PipelineMap):
        def __init__(self, fds):
            self.__fds = fds
        def map(self, pipeline_stream):
            current_count = 0
            continue_yielding = True
            for fd, line in pipeline_stream:
                if current_count >= count:
                    continue_yielding = False
                if continue_yielding or fd not in self.__fds:
                    yield fd, line
                if fd in self.__fds:
                    current_count += 1
    return _Head

def retain(filter_fn):
    """
    Retains only the elements matching filter_fn
    """
    class _Retain(PipelineMap):
        def __init__(self, fds):
            self.__fds = fds
        def map(self, pipeline_stream):
            for fd, line in pipeline_stream:
                if fd not in self.__fds or filter_fn(line):
                    yield fd, line
    return _Retain
