
from os import system
from os.path import join

from shell_extensions_python import ls, pwd, cd, mkdir

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
