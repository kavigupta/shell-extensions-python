import unittest

from shell_extensions_python import s, Collect, sort, FD

from .utilities import reset

class TestMap(unittest.TestCase):
    @reset
    def test_basic_map(self):
        result = s('echo 2; echo 3; echo 4 >&2') | int | (lambda x: x * 2) > Collect
        self.assertEqual([4, 6], result.stdout(raw=True))
        self.assertEqual("4\n", result.stderr())
    @reset
    def test_map_over_err(self):
        result = s('echo 2; echo 3; echo 4 >&2') / int / (lambda x: x * 2) > Collect
        self.assertEqual("2\n3\n", result.stdout())
        self.assertEqual([8], result.stderr(raw=True))
    @reset
    def test_map_over_both_individually(self):
        result = s('echo 2; echo 3; echo 4 >&2') / int / (lambda x: x * 2) | int | (lambda x: x * 10) > Collect
        self.assertEqual([20, 30], result.stdout(raw=True))
        self.assertEqual([8], result.stderr(raw=True))
    @reset
    def test_map_over_both_together(self):
        result = s('echo 2; echo 3; echo 4 >&2') % int % (lambda x: x * 2) > Collect
        self.assertEqual([4, 6], result.stdout(raw=True))
        self.assertEqual([8], result.stderr(raw=True))
    @reset
    def test_invalid_map(self):
        self.assertRaises(RuntimeError, lambda: s('echo 2') | 2)
    @reset
    def test_with_pipeline_mapper_stdout(self):
        result = s('echo 3; echo 2; echo 4 >&2; echo 0 >&2') | sort > Collect
        self.assertEqual("2\n3\n", result.stdout())
        self.assertEqual("4\n0\n", result.stderr())
    @reset
    def test_with_pipeline_mapper_stderr(self):
        result = s('echo 3; echo 2; echo 4 >&2; echo 0 >&2') / sort > Collect
        self.assertEqual("3\n2\n", result.stdout())
        self.assertEqual("0\n4\n", result.stderr())
    @reset
    def test_with_pipeline_mapper_both(self):
        result = s('echo 3; echo 2; echo 4 >&2; echo 0 >&2') % sort > Collect
        self.assertEqual("2\n3\n", result.stdout())
        self.assertEqual("0\n4\n", result.stderr())
        self.assertEqual([(FD.stderr, b"0\n"), (FD.stdout, b"2\n"), (FD.stdout, b"3\n"), (FD.stderr, b"4\n")],
                         list(s('echo 3; echo 2; echo 4 >&2; echo 0 >&2') % sort))
