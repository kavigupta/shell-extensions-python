"""
Contains various functions for searching through strings
"""

import re
import os

from .colors import PrintColors
from .shell_types import ShellStr

class GreppedString(ShellStr):
    """
    A string that represents the results of running grep on a string
    """
    def __new__(cls, components, color):
        result = str.__new__(cls, "".join([component for _, component in components]))
        result.components = components
        result.color = color
        return result
    def __repr__(self):
        result = []
        for is_match, component in self.components:
            result += [self.color if is_match else PrintColors.reset]
            result += [component]
        return ShellStr("".join(result))

def collect_components_for_line(pattern, line):
    """
    Gets the components of a line (whether match components or not)
        pattern: the pattern to match
        line: the line

        output: [(is a match component, component)]
    """
    prev = 0
    for match in re.finditer(pattern, line):
        yield False, line[prev:match.start()]
        yield True, line[match.start():match.end()]
        prev = match.end()
    yield False, line[prev:] + os.linesep

def collect_components(pattern, string, remove_lines):
    """
    Similar to collect_components_for_line but for an entire file
    """
    if string.endswith(os.linesep):
        string = string[:-len(os.linesep)]
    for line in string.split(os.linesep):
        components = list(collect_components_for_line(pattern, line))
        if not remove_lines or any(is_match for is_match, _ in components):
            yield from components

def cgrep(pattern, string, color=PrintColors.red_bright, remove_lines=True):
    """
    Our version of grep
    """
    return GreppedString(list(collect_components(pattern, string, remove_lines)), color)
