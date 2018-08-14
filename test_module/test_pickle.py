
import unittest

from shell_extensions_python import psave, pload, rm
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset

class TestPickle(unittest.TestCase):
    @reset
    def test_pickle(self):
        self.assertEqual(ShellBool.true, psave('test.pkl', [1, 2, 3]))
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')
