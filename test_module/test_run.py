
import unittest

from shell_extensions_python import write, ls, r, re, s, rm, Collect, ProcessFailedException
from shell_extensions_python.run_shell_commands import FD

from .utilities import reset

class TestRun(unittest.TestCase):
    @reset
    def test_chaining(self):
        write('test', '') and write('test2', '')
        self.assertEqual(ls(), ['test', 'test2'])
        rm('test')
        rm('test2')
    @reset
    def test_with_args(self):
        self.assertEqual('-n with space', re('echo', '-n with space', mode=Collect).stdout(single_line=True))
    @reset
    def test_invalid_args(self):
        self.assertRaises(RuntimeError, lambda: r(None))
        self.assertRaises(RuntimeError, lambda: r([['abc']]))
    @reset
    def test_multiple_lines(self):
        self.assertEqual('2\n3\n', r('echo 2; echo 3', mode=Collect).stdout())
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(single_line=True))
        self.assertEqual(['2', '3'], r('echo 2; echo 3', mode=Collect).stdout(as_lines=True))
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(as_lines=True, single_line=True))
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
    @reset
    def test_get_exitcode(self):
        command = s('echo abc')
        self.assertRaises(RuntimeError, lambda: command.exitcode)
    @reset
    def test_collect(self):
        self.assertEqual('abc\n', (s('echo abc') > Collect).stdout())
