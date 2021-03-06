
import unittest

from shell_extensions_python import write, ls, r, re, s, rm, Collect, Stdout, Stderr, Both
from shell_extensions_python.run_shell_commands import FD

from .utilities import reset

class TestRun(unittest.TestCase):
    @reset
    def test_chaining(self):
        write('test', '') and write('test2', '')
        self.assertEqual(ls(), ['test', 'test2'])
        rm('test', 'test2')
    @reset
    def test_with_args(self):
        self.assertEqual('-n with space', re('echo', '-n with space', mode=Collect).stdout(single_line=True))
    @reset
    def test_invalid_args(self):
        self.assertRaises(RuntimeError, lambda: r(None))
        self.assertRaises(RuntimeError, lambda: re(['a']))
    @reset
    def test_multiple_lines(self):
        self.assertEqual('2\n3\n', r('echo 2; echo 3', mode=Collect).stdout())
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(single_line=True))
        self.assertEqual(['2', '3'], r('echo 2; echo 3', mode=Collect).stdout(as_lines=True))
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(as_lines=True, single_line=True))
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(as_lines=True, raw=True))
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(single_line=True, raw=True))
        self.assertRaises(RuntimeError, lambda: r('echo 2; echo 3', mode=Collect).stdout(as_lines=True, single_line=True, raw=True))
    @reset
    def test_raw_output(self):
        self.assertEqual(["2\n", "3\n"], r('echo 2; echo 3', mode=Collect).stdout(raw=True))
        self.assertEqual([b"2\n", b"3\n"], r('echo 2; echo 3', mode=Collect, raw_bytes=True).stdout(raw=True))
        self.assertEqual("2\n3\n", r('echo 2; echo 3', mode=Collect, raw_bytes=True).stdout())
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
        self.assertEqual([(FD.stderr, 'abc\n'), (FD.stdout, 'def\n')], result)
    @reset
    def test_get_exitcode(self):
        command = s('echo abc')
        self.assertRaises(RuntimeError, lambda: command.exitcode)
    @reset
    def test_collect(self):
        self.assertEqual('abc\n', (s('echo abc') > Collect).stdout())
    @reset
    def test_or(self):
        result = r('echo 2; false', mode=Collect) | r('echo 3; true', mode=Collect)
        self.assertEqual('2\n3\n', result.stdout())
        self.assertTrue(result)
    @reset
    def test_and(self):
        result = r('echo 2; false', mode=Collect) & r('echo 3; true', mode=Collect)
        self.assertEqual('2\n3\n', result.stdout())
        self.assertFalse(result)
    @reset
    def test_add(self):
        result = r('echo 2; false', mode=Collect) + r('echo 3; true', mode=Collect)
        self.assertEqual('2\n3\n', result.stdout())
        self.assertTrue(result)
        result = r('echo 2; true', mode=Collect) + r('echo 3; false', mode=Collect)
        self.assertEqual('2\n3\n', result.stdout())
        self.assertFalse(result)

class TestCollectors(unittest.TestCase):
    @reset
    def test_stdout(self):
        self.assertEqual((2, 3, 5), s('echo 2; echo 3; echo 4 >&2; echo 5') % int >= Stdout())
        self.assertEqual({2, 3, 5}, s('echo 2; echo 3; echo 4 >&2; echo 5') % int >= Stdout(set))
    @reset
    def test_stderr(self):
        self.assertEqual((4,), s('echo 2; echo 3; echo 4 >&2; echo 5') % int >= Stderr())
        self.assertEqual({4}, s('echo 2; echo 3; echo 4 >&2; echo 5') % int >= Stderr(set))
    @reset
    def test_stdout_stderr(self):
        self.assertEqual((2, 3, 4, 5), s('echo 2; echo 3; sleep 0.01; echo 4 >&2; sleep 0.01; echo 5') % int >= Both())
        self.assertEqual({2, 3, 4, 5}, s('echo 2; echo 3; sleep 0.01; echo 4 >&2; sleep 0.01; echo 5') % int >= Both(set))
