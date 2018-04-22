# pylint: disable-all

import sys

from .__init__ import *

from .ps1 import SeriesRenderer, UserRenderer, GitPathRenderer, GitStatusRenderer
from .colors import *
from .interactive import modified_displayhook

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

sys.displayhook = modified_displayhook
