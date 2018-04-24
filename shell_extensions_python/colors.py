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

class PrintColors:
    """
    Colors to be printed to the terminal
    """
    yellow_bright = Style.BRIGHT + Fore.YELLOW
    orange = path_color = Fore.YELLOW if windows else "\x1b[38;5;214m"
    green_bright = Style.BRIGHT + Fore.GREEN if windows else  "\x1b[38;5;82m"
    red = Fore.RED
    red_bright = Style.BRIGHT + Fore.RED
    blue = Fore.BLUE
    green = Fore.GREEN if windows else "\x1b[38;5;28m"
    cyan = Fore.BLUE if windows else "\x1b[38;5;38m"
    reset = Style.RESET_ALL

class PS1Colors:
    """
    Colors to be printed for the PS1.
    """
    def __getattr__(self, attr):
        return wrap(getattr(PrintColors, attr))

PS1Colors = PS1Colors()
