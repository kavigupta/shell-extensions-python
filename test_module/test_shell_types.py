
import unittest
from shell_extensions_python.shell_types import ShellBool, ShellStr, ShellList


class TestShellStr(unittest.TestCase):
    def test_lines(self):
        self.assertEqual(['abc'], ShellStr("abc").lines())
        self.assertEqual(['abc', ''], ShellStr("abc\n").lines())
        self.assertEqual(['abc', 'def'], ShellStr("abc\ndef").lines())
        self.assertEqual(ShellList, type(ShellStr("abc\ndef").lines()))
    def test_dirname(self):
        self.assertEqual('', ShellStr("abc").dirname())
        self.assertEqual('abc', ShellStr("abc/").dirname())
        self.assertEqual('abc', ShellStr("abc/def").dirname())
    def test_basename(self):
        self.assertEqual('abc', ShellStr("abc").basename())
        self.assertEqual('', ShellStr("abc/").basename())
        self.assertEqual('def', ShellStr("abc/def").basename())

class TestShellList(unittest.TestCase):
    def test_unlines(self):
        self.assertEqual('abc\ndef', ShellList(['abc', 'def']).unlines())
        self.assertEqual('abc\n', ShellList(['abc', '']).unlines())
        self.assertEqual('abc', ShellList(['abc']).unlines())
        self.assertEqual(ShellStr, type(ShellList(['abc']).unlines()))

class TestShellBool(unittest.TestCase):
    def test_and(self):
        self.assertEqual(ShellBool.true, ShellBool.true & ShellBool.true)
        self.assertEqual(ShellBool.false, ShellBool.false & ShellBool.true)
        self.assertEqual(ShellBool.false, ShellBool.true & ShellBool.false)
        self.assertEqual(ShellBool.false, ShellBool.false & ShellBool.false)
    def test_or(self):
        self.assertEqual(ShellBool.true, ShellBool.true | ShellBool.true)
        self.assertEqual(ShellBool.true, ShellBool.false | ShellBool.true)
        self.assertEqual(ShellBool.true, ShellBool.true | ShellBool.false)
        self.assertEqual(ShellBool.false, ShellBool.false | ShellBool.false)
    def test_xor(self):
        self.assertEqual(ShellBool.false, ShellBool.true ^ ShellBool.true)
        self.assertEqual(ShellBool.true, ShellBool.false ^ ShellBool.true)
        self.assertEqual(ShellBool.true, ShellBool.true ^ ShellBool.false)
        self.assertEqual(ShellBool.false, ShellBool.false ^ ShellBool.false)
