
import unittest

from shell_extensions_python import psave, psaves, pload, ploads, rm
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset

class TestPickle(unittest.TestCase):
    @reset
    def test_pickle(self):
        self.assertEqual(ShellBool.true, psave('test.pkl', [1, 2, 3]))
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')
    @reset
    def test_pickles(self):
        self.assertEqual(ShellBool.true, psaves('test.pkl', [[1, 2, 3], {4 : 5}]))
        self.assertEqual([[1, 2, 3], {4 : 5}], ploads('test.pkl'))
        self.assertEqual([[1, 2, 3]], ploads('test.pkl', limit=1))
        rm('test.pkl')
    @reset
    def test_pload_wrong_size(self):
        self.assertEqual(ShellBool.true, psaves('test.pkl', []))
        self.assertRaises(RuntimeError, lambda: pload('test.pkl'))
        self.assertEqual(ShellBool.true, psaves('test.pkl', [1, 2]))
        self.assertRaises(RuntimeError, lambda: pload('test.pkl'))
        rm('test.pkl')
