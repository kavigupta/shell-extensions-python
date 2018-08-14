
import unittest

from shell_extensions_python import mkdir, rm, ls, write, CannotRemoveDirectoryError, r
from shell_extensions_python.interactive import Interactive
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset

class TestRm(unittest.TestCase):
    @reset
    def test_rm_dne(self):
        self.assertRaises(FileNotFoundError, lambda: rm('does-not-exist'))
        self.assertEqual(ShellBool.true, rm('does-not-exist', ignore_missing=True))
    @reset
    def test_rmdir(self):
        mkdir('empty-folder')
        self.assertEqual(ShellBool.true, rm('empty-folder'))
        self.assertEqual([], ls())
    @reset
    def test_rm_nonemptydir(self):
        mkdir('path')
        write('path/file', 'contents')
        self.assertRaises(CannotRemoveDirectoryError, lambda: rm('path', interactive=False))
        self.assertEqual(['path'], ls())
        self.assertEqual(ShellBool.true, rm('path', recursively=True))
        self.assertEqual([], ls())
        mkdir('path')
        write('path/file', '')
        Interactive.ask_question = lambda _: "n"
        self.assertEqual(ShellBool.false, rm('path'))
        self.assertEqual(['path'], ls())
        Interactive.ask_question = lambda _: "y"
        self.assertEqual(ShellBool.true, rm("path"))
        self.assertEqual([], ls())
    @reset
    def test_rm_symlink(self):
        r('ln -s . link')
        self.assertRaises(RuntimeError, lambda: rm('link'))
        r('rm link')
