
import unittest

from shell_extensions_python import glob, globs, write, rm

from .utilities import reset

class TestGlobs(unittest.TestCase):
    @reset
    def test_glob_empty(self):
        self.assertEqual([], globs("*"))
        self.assertRaises(RuntimeError, lambda: glob("*"))
    @reset
    def test_glob_single(self):
        write('file', 'contents')
        write('second_file', 'contents')
        self.assertEqual(['file'], globs("f*"))
        self.assertEqual('file', glob("f*"))
        rm('file', 'second_file')
    @reset
    def test_glob_multiple(self):
        write('file', 'contents')
        write('second_file', 'contents')
        self.assertEqual(['file', 'second_file'], globs("*f*"))
        self.assertRaises(RuntimeError, lambda: glob("*f*"))
        rm('file', 'second_file')
