
from os.path import expanduser, join
from os import system
import unittest
from random import randint

from shell_extensions_python import cd, pwd, ls, mkdir, cat, write, rm, pload, psave, r, CannotRemoveDirectoryError

INITIAL_PWD = join(pwd(), 'tests')
def reset(fn):
    def modified(self, *args):
        cd(INITIAL_PWD)
        cd('..')
        system('rm -r tests')
        mkdir('tests')
        cd('tests')
        fn(self, *args)
        self.assertEqual(INITIAL_PWD, pwd())
        self.assertEqual(ls(), [])
    return modified

class Tests(unittest.TestCase):

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
        self.assertEqual(cat('path/to/folder/file.txt'), "hello")
        rm('path', recursively=True)

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
    def test_pickle(self):
        psave('test.pkl', [1, 2, 3])
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')

    @reset
    def test_exit_code(self):
        self.assertEqual(True, bool(r('true')))
        self.assertEqual(False, bool(r('false')))

if __name__ == '__main__':
    unittest.main()
