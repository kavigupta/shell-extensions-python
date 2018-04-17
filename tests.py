
from os.path import expanduser, join
from os import system
import unittest

from shell_extensions_python import cd, pwd, ls, mkdir, cat, write, rm, pload, psave

system('rm -r tests/* tests/.*')
mkdir('tests')
INITIAL_PWD = join(pwd(), 'tests')
def reset(fn):
    def modified(*args):
        cd(INITIAL_PWD)
        fn(*args)
    return modified

class Tests(unittest.TestCase):

    @reset
    def test_basic_cd(self):
        initial = pwd()
        cd()
        self.assertEqual(expanduser("~"), pwd())
        cd(1)
        self.assertEqual(initial, pwd())
    @reset
    def test_empty_ls(self):
        self.assertEqual(ls(), [])
    @reset
    def test_add_file(self):
        write('test.py', 'hi!!!')
        self.assertEqual(ls(), ['test.py'])
        self.assertEqual(cat('test.py'), 'hi!!!')
        rm('test.py')
        self.assertEqual(ls(), [])
    @reset
    def test_pickle(self):
        psave('test.pkl', [1, 2, 3])
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')


if __name__ == '__main__':
    unittest.main()
