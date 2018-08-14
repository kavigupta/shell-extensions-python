
from os.path import expanduser, join
from os import system
import unittest
from random import randint
from time import sleep

from shell_extensions_python import cd, pwd, ls, mkdir, cat, write, rm, mv, pload, psave, r, s, CannotRemoveDirectoryError

from shell_extensions_python.tcombinator import TCombinator

from shell_extensions_python.shell_types import ShellBool
from shell_extensions_python.interactive import Interactive
from shell_extensions_python.run_shell_commands import FD

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
        self.assertEqual(cat('path/to/folder/file.txt'), "hello")
        rm('path', recursively=True)
    @reset
    def test_return_code(self):
        mkdir('path')
        self.assertEqual(ShellBool.true, cd('path'))
        self.assertEqual(ShellBool.true, cd('..'))
        self.assertRaises(FileNotFoundError, lambda: cd('does-not-exist'))
        rm('path')


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

class TestWrite(unittest.TestCase):
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
    def test_Return_value(self):
        self.assertEqual(ShellBool.true, write('hi', 'hi'))
        rm('hi')

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

class TestPickle(unittest.TestCase):
    @reset
    def test_pickle(self):
        self.assertEqual(ShellBool.true, psave('test.pkl', [1, 2, 3]))
        self.assertEqual(pload('test.pkl'), [1, 2, 3])
        rm('test.pkl')

class TestRun(unittest.TestCase):
    @reset
    def test_chaining(self):
        write('test', '') and write('test2', '')
        self.assertEqual(ls(), ['test', 'test2'])
        rm('test')
        rm('test2')
    @reset
    def test_exit_code(self):
        self.assertEqual(True, bool(r('true')))
        self.assertEqual(False, bool(r('false')))
    @reset
    def test_return_value(self):
        self.assertEqual("", repr(r('true')))
    @reset
    def test_callback_order(self):
        result = list(s('echo abc >&2; sleep 0.1; echo def'))
        self.assertEqual([(FD.stderr, b'abc\n'), (FD.stdout, b'def\n')], result)


class TestCp(unittest.TestCase):
    @reset
    def test_cp(self):
        self.fail("This is not covered")

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

class TestTCombinator(unittest.TestCase):
    def test_temporal_zip(self):
        def generator1():
            sleep(0.1)
            yield 1
            sleep(0.2)
            yield 3
            sleep(0.2)
            yield 5
        def generator2():
            sleep(0.2)
            yield 2
            sleep(0.2)
            yield 4
        self.assertEqual([1, 2, 3, 4, 5], list(TCombinator(generator1(), generator2())))

if __name__ == '__main__':
    unittest.main()
