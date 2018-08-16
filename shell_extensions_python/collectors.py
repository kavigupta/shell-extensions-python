"""
Classes collecting outputs
"""

from .fd import FD

class CollectOutput:
    """
    Collects the outputs corresponding to the given file descriptors into the given datatype
    """
    def __init__(self, dtype, fds):
        self.__dtype = dtype
        self.__fds = fds
    def __call__(self, pipeline):
        results = self.__dtype(line for fd, line in pipeline if fd in self.__fds)
        return results

class Stdout(CollectOutput):
    """
    Collects standard out into the given datatype
    """
    def __init__(self, dtype=tuple):
        super().__init__(dtype, {FD.stdout})

class Stderr(CollectOutput):
    """
    Collects standard error into the given datatype
    """
    def __init__(self, dtype=tuple):
        super().__init__(dtype, {FD.stderr})

class Both(CollectOutput):
    """
    Collects all outputs into the given datatype
    """
    def __init__(self, dtype=tuple):
        super().__init__(dtype, {FD.stdout, FD.stderr})
