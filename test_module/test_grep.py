
import unittest

from shell_extensions_python import cgrep
from shell_extensions_python.colors import PrintColors

from .utilities import reset

class TestLs(unittest.TestCase):
    @reset
    def test_basic_grep(self):
        self.assertEqual("{1}h{0}e{1}ll{0}o{1}\n{1}bcd\n".format(PrintColors.red_bright, PrintColors.reset),
                         repr(cgrep("[aeiou]", "hello\nbcd", remove_lines=False, color=PrintColors.red_bright)))
    @reset
    def test_basic_grep_ends_with_nl(self):
        self.assertEqual("{1}h{0}e{1}ll{0}o{1}\n{1}bcd\n".format(PrintColors.red_bright, PrintColors.reset),
                         repr(cgrep("[aeiou]", "hello\nbcd\n", remove_lines=False, color=PrintColors.red_bright)))
    @reset
    def test_removed_lines_grep(self):
        self.assertEqual("{1}h{0}e{1}ll{0}o{1}\n".format(PrintColors.red_bright, PrintColors.reset),
                         repr(cgrep("[aeiou]", "hello\nbcd", remove_lines=True, color=PrintColors.red_bright)))
