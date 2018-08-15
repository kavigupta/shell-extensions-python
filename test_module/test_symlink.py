
import unittest

from shell_extensions_python import mkdir, rm, symlink, ls, write, cat

from .utilities import reset

class TestSymlink(unittest.TestCase):
    @reset
    def test_basic_symlink(self):
        write('file', 'contents')
        symlink('file', 'link')
        self.assertEqual('contents', cat('link'))
        rm('file', 'link')
    @reset
    def test_basic_symlink_to_folder(self):
        mkdir('folder')
        write('folder/file', 'contents')
        symlink('folder/file', 'link')
        self.assertEqual('contents', cat('folder/file'))
        rm('link')
        rm('folder', recursively=True)
    @reset
    def test_symlink_overwrite_link(self):
        write('file1', 'first contents')
        write('file2', 'second contents')
        symlink('file1', 'link')
        self.assertRaises(RuntimeError, lambda: symlink('file2', 'link'))
        self.assertEqual('first contents', cat('link'))
        symlink('file2', 'link', overwrite=True)
        self.assertEqual('second contents', cat('link'))
        rm('file1', 'file2', 'link')
    @reset
    def test_symlink_overwrite_folder(self):
        write('file', 'contents')
        mkdir('folder')
        self.assertRaises(RuntimeError, lambda: symlink('file', 'folder'))
        self.assertRaises(RuntimeError, lambda: symlink('file', 'folder', overwrite=True))
        self.assertEqual([], ls('folder'))
        rm('file', 'folder')
    @reset
    def test_symlink_to_nonexistant(self):
        self.assertRaises(FileNotFoundError, lambda: symlink('nonexistant', 'link'))
        symlink('nonexistant', 'link', ignore_missing=True)
        write('nonexistant', 'contents')
        self.assertEqual('contents', cat('link'))
        rm('nonexistant', 'link')
