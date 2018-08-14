
import unittest

from shell_extensions_python import write, ls, r, s, rm
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
