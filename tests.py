
from os.path import expanduser, join
from os import system
import unittest

from shell_extensions_python import cd, pwd, ls, mkdir, cat, write, rm, pload, psave

system('rm -r tests')
mkdir('tests')
INITIAL_PWD = join(pwd(), 'tests')
def reset(fn):
    def modified(self, *args):
        cd(INITIAL_PWD)
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
        rm('path', remove_recursively=True)

    @reset
    def test_empty_ls(self):
        self.assertEqual(ls(), [])
    @reset
    def test_add_file(self):
        write('test.py', 'hi!!!')
        self.assertEqual(ls(), ['test.py'])
        self.assertEqual(cat('test.py'), 'hi!!!')
        rm('test.py')
    @reset
    def test_pickle(self):
        psave('test.pkl', [1, 2, 3])
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')


if __name__ == '__main__':
    unittest.main()
