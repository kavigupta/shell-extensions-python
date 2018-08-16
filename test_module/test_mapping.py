
import unittest

from shell_extensions_python import s, col, cols, Stdout

from .utilities import reset

class TestMapping(unittest.TestCase):
    @reset
    def test_col_basic(self):
        self.assertEqual(('3',), s('echo 2 3 4') | str.split | col(1) >= Stdout())
    @reset
    def test_col_with_type(self):
        self.assertEqual((3,), s('echo 2 3 4') | str.split | col(1, int) >= Stdout())
    @reset
    def test_cols_basic(self):
        self.assertEqual((('3',),), s('echo 2 3 4') | str.split | cols(1) >= Stdout())
        self.assertEqual((('3', '4'),), s('echo 2 3 4') | str.split | cols(1, 2) >= Stdout())
    @reset
    def test_cols_with_type(self):
        self.assertEqual(((3,),), s('echo 2 3 4') | str.split | cols((1, int)) >= Stdout())
        self.assertEqual(((3.0, 4),), s('echo 2 3 4') | str.split | cols((1, float), (2, int)) >= Stdout())
