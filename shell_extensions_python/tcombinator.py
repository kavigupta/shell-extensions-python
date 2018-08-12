"""
Provides TCombinator.
"""

from threading import Semaphore, Lock, Thread

class SIGSEGV:
    """
    If you're happy and you know it...
    """
    pass
SIGSEGV = SIGSEGV()

class EOF:
    """
    Represents the end of a file
    """
EOF = EOF()

class TCombinator:
    """
    Takes in any number of asynchronous generators and is an iterable that produces a value
        whenever any of the generators produces a value.

    For usage examples, see ../tests.py:TestTCombinator
    """
    def __init__(self, *generators):
        self.buffer = SIGSEGV
        self.spaces_available = Semaphore(1)
        self.items_present = Semaphore(0)
        self.n_threads = len(generators)
        for generator in generators:
            thread = Thread(target=self._thread, args=[generator])
            thread.start()

    def _thread(self, generator):
        """
        A thread that consumes the given generator and pushes each value onto the stack
        """
        while True:
            try:
                item = next(generator)
            except StopIteration:
                item = EOF
            self.spaces_available.acquire()
            self.buffer = item
            self.items_present.release()
            if item == EOF:
                break

    def __iter__(self):
        threads_remaining = self.n_threads
        while True:
            self.items_present.acquire()
            item = self.buffer
            assert item is not SIGSEGV
            if item != EOF:
                yield self.buffer
                self.buffer = SIGSEGV
            else:
                threads_remaining -= 1
            self.spaces_available.release()
            if threads_remaining == 0:
                break
