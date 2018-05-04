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
        self.thread_done_lock = Lock()
        self.threads_remaining = len(generators)
        for generator in generators:
            thread = Thread(target=self._thread, args=[generator])
            thread.start()

    def _thread(self, generator):
        """
        A thread that consumes the given generator and pushes each value onto the stack
        """
        for item in generator:
            self.spaces_available.acquire()
            self.buffer = item
            self.items_present.release()
        with self.thread_done_lock:
            self.threads_remaining -= 1

    def __iter__(self):
        while True:
            with self.thread_done_lock:
                if self.threads_remaining == 0:
                    break
            self.items_present.acquire()
            assert self.buffer is not SIGSEGV
            yield self.buffer
            self.buffer = SIGSEGV
            self.spaces_available.release()
