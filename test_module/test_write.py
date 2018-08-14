
import unittest

from shell_extensions_python import write, ls, cat, rm
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset

class TestWrite(unittest.TestCase):
    @reset
    def test_add_file(self):
        write('test.py', 'hi!!!')
        self.assertEqual(ls(), ['test.py'])
        self.assertEqual(cat('test.py'), 'hi!!!')
        rm('test.py')
    @reset
    def test_write_options(self):
        write('test', 'first line\n')
        self.assertEqual(ls(), ['test'])
        self.assertEqual(cat('test'), 'first line\n')
        self.assertRaises(FileExistsError, lambda: write('test', 'first line\n'))
        write('test', 'first line modified\n', clobber=True)
        self.assertEqual(cat('test'), 'first line modified\n')
        write('test', 'second line\n', append=True)
        self.assertEqual(cat('test'), 'first line modified\nsecond line\n')
        rm('test')
    @reset
    def test_Return_value(self):
        self.assertEqual(ShellBool.true, write('hi', 'hi'))
        rm('hi')
    @reset
    def test_argument_conflict(self):
        self.assertRaises(ValueError, lambda: write('hi', 'hi', clobber=True, append=True))
