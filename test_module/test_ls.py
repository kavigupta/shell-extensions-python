
import unittest

from random import randint

from shell_extensions_python import ls, cd, rm, mkdir, write

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
        rm("shown")
        rm(".hidden")
    @reset
    def test_sorted_ls(self):
        paths = [hex(randint(0, 0x10000000000)) for _ in range(50)]
        for path in paths:
            write(path, '')
        self.assertEqual(sorted(paths), ls())
        for path in paths:
            rm(path)
