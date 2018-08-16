
import unittest

from shell_extensions_python import write, cat, Collect, rm, mkdir

from .utilities import reset

class TestCat(unittest.TestCase):
    @reset
    def test_read_succeed(self):
        write('file', 'contents\nline 2')
        self.assertEqual('contents\nline 2', (cat('file') > Collect).stdout())
        write('file', 'contents\n', clobber=True)
        self.assertEqual('contents\n', (cat('file') > Collect).stdout())
        rm('file')
    @reset
    def test_read_fail(self):
        result = cat('nonexistant') > Collect
        self.assertEqual(False, bool(result))
        self.assertIn("No such file", result.stderr())
        mkdir('folder')
        result = cat('folder') > Collect
        self.assertEqual(False, bool(result))
        self.assertIn("Is a directory", result.stderr())
        rm('folder')
