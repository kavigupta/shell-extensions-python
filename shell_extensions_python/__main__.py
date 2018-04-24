# pylint: disable-all

import sys

from .__init__ import *

from .ps1 import SeriesRenderer, UserRenderer, GitPathRenderer, GitStatusRenderer
from .colors import PS1Colors
from .interactive import modified_displayhook

SeriesRenderer(
    UserRenderer(user_color=PS1Colors.yellow_bright),
    " ",
    GitPathRenderer(outside_color=PS1Colors.orange, repo_color=PS1Colors.green_bright, local_color=PS1Colors.green),
    " ",
    GitStatusRenderer(modified=PS1Colors.orange, new=PS1Colors.green_bright, deleted=PS1Colors.red, staged=PS1Colors.blue, behind=PS1Colors.red, ahead=PS1Colors.green_bright, branch_color=PS1Colors.cyan),
    " $ "
).set()

from colorama import init
init()
del init

sys.displayhook = modified_displayhook
