
import unittest

from shell_extensions_python.autorun import autorun

class TestAutoRun(unittest.TestCase):
    def test_autorun(self):
        @autorun
        def f():
            return 2
        self.assertEqual(2, f.__repr_proxy__())
