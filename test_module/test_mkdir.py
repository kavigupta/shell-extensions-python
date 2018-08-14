
import unittest

from shell_extensions_python import mkdir, rm
from shell_extensions_python.shell_types import ShellBool

from .utilities import reset

class TestMkdir(unittest.TestCase):
    @reset
    def test_mkdir(self):
        self.assertEqual(ShellBool.true, mkdir('folder'))
        self.assertEqual(ShellBool.false, mkdir('folder'))
        rm('folder')
