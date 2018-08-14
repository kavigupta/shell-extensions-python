
from time import sleep
import unittest

from shell_extensions_python.tcombinator import TCombinator

class TestTCombinator(unittest.TestCase):
    def test_temporal_zip(self):
        def generator1():
            sleep(0.1)
            yield 1
            sleep(0.2)
            yield 3
            sleep(0.2)
            yield 5
        def generator2():
            sleep(0.2)
            yield 2
            sleep(0.2)
            yield 4
        self.assertEqual([1, 2, 3, 4, 5], list(TCombinator(generator1(), generator2())))
