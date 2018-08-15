"""
A simple interface to git
"""

from enum import Enum
from collections import namedtuple

from .run_shell_commands import re, Collect, throw, ProcessFailedException
from .basic_shell_programs import pwd
from .shell_types import ShellBool

class NoRepositoryError(RuntimeError):
    """
    Not in a repository
    """
    pass

def current_repository():
    """
    Get a path to the current repository or raise an error
    """
    result = re('git', 'rev-parse', '--show-toplevel', mode=Collect) or throw(NoRepositoryError)
    return result.stdout(single_line=True)

def check_in_repository(func):
    """
    Confirms that you are in a repository and if not, raises a NoRepositoryError
    """
    def modified(*args, **kwargs):
        """
        The modified function
        """
        current_repository()
        return func(*args, **kwargs)
    return modified

@check_in_repository
def relative_path_in_repository():
    """
    Gets our path relative to the repository
    """
    git_directory = current_repository()
    if git_directory is None:
        return ""
    local = pwd()[len(git_directory):]
    return local

@check_in_repository
def current_branch():
    """
    Get the current branch we are on as a string
    """
    result = re('git', 'rev-parse', '--abbrev-ref', 'HEAD', mode=Collect)
    return result.stdout(single_line=True)

class NoTrackingBranchError(OSError):
    """
    An error representing that there's no tracking branch
    """
    pass

@check_in_repository
def tracking_branch():
    """
    Get the branch we are tracking
    """
    symbolic = re('git', 'symbolic-ref', '-q', 'HEAD', mode=Collect) or throw(ProcessFailedException)
    current_symbol_ref = symbolic.stdout(single_line=True)
    upstream = re('git', 'for-each-ref', "--format=%(upstream:short)", current_symbol_ref, mode=Collect)
    output = upstream.stdout(as_lines=True)
    assert len(output) <= 1, str(output)
    if not output:
        raise NoTrackingBranchError
    return output[0]

@check_in_repository
def set_tracking_branch(to_track):
    """
    Sets the branch this branch is tracking
    """
    re('git', 'branch', '-u', to_track)

@check_in_repository
def commits_wrt_tracking():
    """
    Get the number of commits off from the tracking branch (ahead, behind)
    """
    try:
        result = re('git',
                    'rev-list',
                    '--left-right',
                    '--count',
                    current_branch() + "..." + tracking_branch(),
                    mode=Collect) or throw(ProcessFailedException)
        ahead, behind = result.stdout(single_line=True).split()
        return int(ahead), int(behind)
    except NoTrackingBranchError:
        return 0, 0

@check_in_repository
def status():
    """
    Literally just run git status
    """
    re('git', 'status')

class GitStatusCategory(Enum):
    """
    Represents the status of a file.
    """
    modified = 0
    added = 1
    deleted = 2
    staged = 3
    other = 4

class FileStatus(namedtuple('FileStatus', ['staged_status', 'unstaged_status'])):
    """
    Represents a file's status
    """
    @staticmethod
    def of(line):
        """
        Takes in a porcelain line and returns a tuple (status, path)
        """
        staged_unstaged = line[:2].replace(" ", "~")
        return FileStatus(staged_unstaged[0], staged_unstaged[1]), line[3:]
    def category(self):
        """
        Returns this given status's category
        """
        if self.staged_status not in "~?":
            return GitStatusCategory.staged
        if self.unstaged_status == "M":
            return GitStatusCategory.modified
        if self.unstaged_status == "?":
            return GitStatusCategory.added
        if self.unstaged_status == "D":
            return GitStatusCategory.deleted
        return GitStatusCategory.other
    def status_str(self):
        """
        Returns our status as a string
        """
        return self.staged_status + self.unstaged_status

def status_summary():
    """
    Ouput a list [(status, path)] for all files that would be output by git status.
    """
    results = []
    for line in (re('git', 'status', '--porcelain', mode=Collect) \
                        or throw(ProcessFailedException)).stdout(as_lines=True):
        line = line.strip('\r\n')
        if not line:
            continue
        results.append(FileStatus.of(line))
    return results

def push(remote=None, branch=None):
    """
    Calls git push
    """
    command = ['git', 'push']
    if remote is not None:
        command.append(remote)
    if branch is not None:
        command.append(branch)
    return re(*command)

def init():
    """
    Calls git init
    """
    return re('git', 'init')

def add(*paths):
    """
    Calls git add
    """
    return re('git', 'add', *paths)

def reset():
    """
    Calls git reset
    """
    return re('git', 'reset')

def show_staged():
    """
    Calls git diff --staged, shows staged changes
    """
    return re('git', 'diff', '--staged')

def commit(message, review=False):
    """
    Calls git commit -m

    If review is True, it shows you what you are about to stage
        and asks you if you want to continue
    """
    if review:
        show_staged()
        if not input("Do you want to commit? [yN] ") == "y":
            return ShellBool.false
    return re('git', 'commit', '-m', message)

def pull_ff():
    """
    Calls git commit --ff-only. Returns False if it doesn't succeed.
    """
    return bool(re('git', 'pull', '--ff-only'))

def diff(*paths):
    """
    Calls diff on the given paths.
    """
    if not paths:
        paths = ['.']
    return re('git', 'diff', *paths)
