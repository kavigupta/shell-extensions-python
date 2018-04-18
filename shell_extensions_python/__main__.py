# pylint: disable-all

from shell_extensions_python import *

from shell_extensions_python.ps1 import SeriesRenderer, UserRenderer, GitPathRenderer, GitStatusRenderer
from colors import *

SeriesRenderer(
    UserRenderer(user_color=yellow_bright),
    " ",
    GitPathRenderer(outside_color=orange, repo_color=green_bright, local_color=green),
    " ",
    GitStatusRenderer(modified=orange, new=green_bright, deleted=red, staged=blue, behind=red, ahead=green_bright, branch_color=cyan),
    " $ "
).set()

from colorama import init
init()
del init
