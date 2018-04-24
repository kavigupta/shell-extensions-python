"""
Several extensions for python to be usable as a bash-style shell.
"""

import sys

from abc import ABCMeta, abstractmethod

from collections import Counter

import shell_extensions_python.git as git
from .git import GitStatusCategory

from .colors import PS1Colors


from .basic_shell_programs import pwd, whoami

from .path_manipulation import unexpand_user, basename, dirname

class Renderer(metaclass=ABCMeta):
    """
    Base class of PS1 classes
    """
    @abstractmethod
    def render(self):
        """
        Renders the current state of the universe as a string with color codes
        """
        pass
    def set(self):
        """
        Set this as the PS1
        """
        sys.ps1 = self
    def __str__(self):
        return self.render()

class GitPathRenderer(Renderer):
    """
    A renderer that renders the path with different colors for the git directory
    """
    def __init__(self, outside_color, repo_color, local_color):
        self.outside_color = outside_color
        self.repo_color = repo_color
        self.local_color = local_color
    @staticmethod
    def current_repository_split():
        """
        Return the path of the current repository, split into the parent of the repository,
            and the repository's exact name
        """
        git_directory = git.current_repository()
        above = unexpand_user(dirname(git_directory))
        in_directory = basename(git_directory)
        return above, "/" + in_directory
    def render(self):
        try:
            above, repo = GitPathRenderer.current_repository_split()
            local = git.relative_path_in_repository()
            return self.outside_color + above + self.repo_color + repo + self.local_color + local + PS1Colors.reset
        except git.NoRepositoryError:
            return self.outside_color + pwd() + PS1Colors.reset

class GitStatusRenderer(Renderer):
    """
    Renders git's current status in the form
        branch [-behind tracking, +ahead tracking] <status wrt master>
    """
    #pylint: disable=too-many-arguments
    def __init__(self, modified, new, deleted, staged, behind, ahead, branch_color):
        self.modified = modified
        self.new = new
        self.deleted = deleted
        self.staged = staged
        self.behind = behind
        self.ahead = ahead
        self.branch_color = branch_color
    def render_branch(self):
        """
        Render the current branch
        """
        branch = git.current_branch()
        return self.branch_color + branch + PS1Colors.reset
    def git_offsets(self):
        """
        Render the offsets with respect to the tracking branch
        """
        ahead, behind = git.commits_wrt_tracking()
        newoffs = []
        if behind:
            newoffs.append(self.behind + "-" + str(behind))
        if ahead:
            newoffs.append(self.ahead + "+" + str(ahead))
        result = ", ".join(newoffs)
        if result == "":
            return ""
        return PS1Colors.reset + " [" + result + PS1Colors.reset + "]"
    def process_status(self, prefix, count):
        """
        Colors the given status and count, and places an @ in between
        """
        item_color = {
            GitStatusCategory.modified : self.modified,
            GitStatusCategory.added : self.new,
            GitStatusCategory.deleted : self.deleted,
            GitStatusCategory.staged : self.staged,
            GitStatusCategory.other : PS1Colors.reset
        }[prefix.category()]
        return item_color + prefix.status_str() + "@" + str(count) + PS1Colors.reset
    def one_line_status(self):
        """
        Prints out a one-line representation of the status of the git repository
        """
        prefixes = sorted(Counter(stat for stat, _ in git.status_summary()).items())
        summary = " ".join(self.process_status(prefix, count) for prefix, count in prefixes)
        if not summary:
            return ""
        return PS1Colors.reset + " <" + summary + PS1Colors.reset + ">"
    def render(self):
        try:
            return self.render_branch() + self.git_offsets() + self.one_line_status()
        except git.NoRepositoryError:
            return ""

class UserRenderer(Renderer):
    """
    Renders the user
    """
    def __init__(self, user_color):
        self.user_color = user_color
    def render(self):
        return self.user_color + whoami() + PS1Colors.reset

class ConstRenderer(Renderer):
    """
    Renders the given element
    """
    def __init__(self, element):
        self.element = element
    def render(self):
        return self.element

class SeriesRenderer(Renderer):
    """
    Renders its arguments in series
    """
    def __init__(self, *renderers):
        self.renderers = [ConstRenderer(x) if isinstance(x, str) else x for x in renderers]
    def render(self):
        return "".join(x.render() for x in self.renderers)
