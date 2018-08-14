
import unittest

from shell_extensions_python import whoami
from shell_extensions_python.path_manipulation import expand_user, unexpand_user

from .utilities import reset

class TestPathManipulation(unittest.TestCase):
    @reset
    def test_expand_user(self):
        self.assertEqual("/home/%s/abc/def" % whoami(), expand_user("~/abc/def"))
    @reset
    def test_unexpand_user(self):
        self.assertEqual("~/abc/def", unexpand_user("/home/%s/abc/def" % whoami()))
