
import unittest

from random import randint

from shell_extensions_python import ls, cd, rm, mkdir, write, r
from shell_extensions_python.interactive import FileType, DisplayPath

from .utilities import reset

class TestLs(unittest.TestCase):
    @reset
    def test_empty_ls(self):
        self.assertEqual(ls(), [])
    @reset
    def test_full_path_ls(self):
        mkdir('path/to')
        write('path/to/file.txt', 'contents')
        self.assertEqual(ls('path'), ['to'])
        self.assertEqual(ls('path', full=True), ['path/to'])
        cd('path')
        self.assertEqual(ls('..'), ['path'])
        self.assertEqual(ls('..', full=True), ['../path'])
        cd('..')
        rm('path', recursively=True)
    @reset
    def test_all_ls(self):
        write("shown", '')
        write(".hidden", '')
        self.assertEqual(ls(), [".hidden", "shown"])
        self.assertEqual(ls(a=False), ["shown"])
        rm("shown", ".hidden")
    @reset
    def test_sorted_ls(self):
        paths = [hex(randint(0, 0x10000000000)) for _ in range(50)]
        for path in paths:
            write(path, '')
        self.assertEqual(sorted(paths), ls())
        rm(*paths)
    @reset
    def test_colors(self):
        write('file', 'contents')
        mkdir('folder')
        write('deleted', 'to be deleted')
        write('executable', 'to be deleted')
        r('ln -s file link')
        r('chmod +x executable')
        deleted, executable, file, folder, link = ls()
        rm('deleted')
        self.assertEqual(FileType.normal_file, deleted.type)
        self.assertEqual(FileType.normal_file, file.type)
        self.assertEqual(FileType.executable, executable.type)
        self.assertEqual(FileType.directory, folder.type)
        self.assertEqual(FileType.link, link.type)
        rm('file', 'folder', 'executable')
        r('rm link')
    @reset
    def test_missing(self):
        self.assertEqual(FileType.missing, DisplayPath("nonexistant", ".").type)
