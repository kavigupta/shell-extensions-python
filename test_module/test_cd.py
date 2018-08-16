
from os.path import expanduser, join

import unittest

from shell_extensions_python import pwd, cd, rm, write, read, mkdir
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset, INITIAL_PWD

class TestCd(unittest.TestCase):
    @reset
    def test_basic_cd(self):
        cd()
        self.assertEqual(expanduser("~"), pwd())
        cd(1)
    @reset
    def test_more_complicated_cd(self):
        mkdir('path/to/folder')
        cd('path')
        self.assertEqual(join(INITIAL_PWD, 'path'), pwd())
        cd('..')
        self.assertEqual(INITIAL_PWD, pwd())
        cd('path/to')
        self.assertEqual(join(INITIAL_PWD, 'path/to'), pwd())
        cd('.')
        self.assertEqual(join(INITIAL_PWD, 'path/to'), pwd())
        cd('..')
        self.assertEqual(join(INITIAL_PWD, 'path'), pwd())
        cd('to/folder')
        self.assertEqual(join(INITIAL_PWD, 'path/to/folder'), pwd())
        write('file.txt', "hello")
        cd(3)
        self.assertEqual(join(INITIAL_PWD, 'path/to'), pwd())
        cd(1)
        self.assertEqual(INITIAL_PWD, pwd())
        cd(1)
        self.assertEqual(join(INITIAL_PWD, 'path'), pwd())
        cd(INITIAL_PWD)
        self.assertEqual(read('path/to/folder/file.txt'), "hello")
        rm('path', recursively=True)
    @reset
    def test_return_code(self):
        mkdir('path')
        self.assertEqual(ShellBool.true, cd('path'))
        self.assertEqual(ShellBool.true, cd('..'))
        self.assertRaises(FileNotFoundError, lambda: cd('does-not-exist'))
        rm('path')
    @reset
    def test_invalid_cd_argument(self):
        cd.stack = [pwd(), pwd()]
        self.assertRaises(RuntimeError, lambda: cd(0))
        self.assertRaises(RuntimeError, lambda: cd(2))
        self.assertRaises(RuntimeError, lambda: cd(3))
        self.assertEqual([pwd(), pwd()], cd.stack)
        cd(1)
        self.assertRaises(TypeError, lambda: cd(None))
