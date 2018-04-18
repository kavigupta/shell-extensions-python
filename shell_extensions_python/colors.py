"""
Several colors used in PS1s and elsewhere. This provides unix terminal codes
    and windows alternatives from colorama
"""
#pylint: disable=invalid-name
import os

from colorama import Fore, Style


windows = os.name == 'nt'

def wrap(color_seq):
    """
    Wrap the given color sequence to tell the terminal that unprintable characters are unprintable
    """
    return "\001%s\002" % color_seq

yellow_bright = wrap(Style.BRIGHT + Fore.YELLOW)
orange = path_color = wrap(Fore.YELLOW if windows else "\x1b[38;5;214m")
green_bright = wrap(Style.BRIGHT + Fore.GREEN if windows else  "\x1b[38;5;82m")
red = wrap(Fore.RED)
blue = wrap(Fore.BLUE)
green = wrap(Fore.GREEN if windows else "\x1b[38;5;28m")
cyan = wrap(Fore.BLUE if windows else "\x1b[38;5;38m")
reset = wrap(Style.RESET_ALL)
