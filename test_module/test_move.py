
import unittest

from shell_extensions_python import mv, move_to, write, mkdir, ls, cat, rm

from .utilities import reset

class TestMv(unittest.TestCase):
    @reset
    def test_mv_nonexistant(self):
        self.assertRaises(FileNotFoundError, lambda: mv('nonexistant', 'dst'))
    @reset
    def test_mv_dst_folder(self):
        write('src', 'abc')
        mkdir('folder')
        self.assertRaises(RuntimeError, lambda: mv('src', 'folder'))
        rm('folder')
        rm('src')
    @reset
    def test_mv_dst_exists(self):
        write('src', 'abc')
        write('file', 'def')
        self.assertRaises(RuntimeError, lambda: mv('src', 'file'))
        self.assertEqual(['file', 'src'], ls())
        mv('src', 'file', overwrite=True)
        self.assertEqual(['file'], ls())
        self.assertEqual('abc', cat('file'))
        rm('file')
    @reset
    def test_mv_dst_folder_doesnt_exist(self):
        write('src', 'abc')
        mv('src', 'folder/file')
        self.assertEqual(['folder'], ls())
        self.assertEqual(['file'], ls('folder'))
        self.assertEqual('abc', cat('folder/file'))
        mv('folder/file', 'folder/to/a/file')
        self.assertEqual(['folder'], ls())
        self.assertEqual(['to'], ls('folder'))
        self.assertEqual(['a'], ls('folder/to'))
        self.assertEqual(['file'], ls('folder/to/a'))
        self.assertEqual('abc', cat('folder/to/a/file'))
        rm('folder', recursively=True)
    @reset
    def test_mv_dst_folder_doesnt_exist_create_dir_false(self):
        write('src', 'abc')
        self.assertRaises(RuntimeError, lambda: mv('src', 'folder/file', create_dir=False))
        rm('src')

class TestMoveTo(unittest.TestCase):
    @reset
    def test_mv_single_file_to_existing_folder(self):
        write('file', 'contents')
        mkdir('folder')
        move_to('file', 'folder')
        self.assertEqual(['folder'], ls())
        self.assertEqual(['file'], ls('folder'))
        self.assertEqual('contents', cat('folder/file'))
        rm('folder', recursively=True)
    @reset
    def test_mv_single_file_to_nonexistant_folder(self):
        write('file', 'contents')
        self.assertRaises(RuntimeError, lambda: move_to('file', 'folder', create_dir=False))
        move_to('file', 'folder')
        self.assertEqual(['folder'], ls())
        self.assertEqual(['file'], ls('folder'))
        self.assertEqual('contents', cat('folder/file'))
        rm('folder', recursively=True)
    @reset
    def test_mv_single_file_to_existant_file(self):
        write('file', 'contents')
        write('other_file', 'contents')
        self.assertRaises(RuntimeError, lambda: move_to('file', 'other_file'))
        rm('file', recursively=True)
        rm('other_file', recursively=True)
