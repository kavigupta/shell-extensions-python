"""
A simple interface to git
"""

from enum import Enum
from collections import namedtuple

from .run_shell_commands import r

from .basic_shell_programs import pwd

class NoRepositoryError(RuntimeError):
    """
    Not in a repository
    """
    pass

def current_repository():
    """
    Get a path to the current repository or raise an error
    """
    result = r(('git', 'rev-parse', '--show-toplevel'), std=True, err=True, throw=NoRepositoryError)
    return result.stdout.decode('utf-8').strip()

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
    result = r(('git', 'rev-parse', '--abbrev-ref', 'HEAD'), std=True, err=True, throw=True)
    return result.stdout.decode('utf-8').strip()

@check_in_repository
def tracking_branch():
    """
    Get the branch we are tracking
    """
    symbolic = r(('git', 'symbolic-ref', '-q', 'HEAD'), std=True, err=True, throw=True)
    current_symbol_ref = symbolic.stdout.decode('utf-8').strip()
    upstream = r((('git', 'for-each-ref', "--format=%(upstream:short)", current_symbol_ref)), std=True, err=True)
    return upstream.stdout.decode('utf-8').strip()

@check_in_repository
def commits_wrt_tracking():
    """
    Get the number of commits off from the tracking branch (ahead, behind)
    """
    result = r(('git', 'rev-list', '--left-right', '--count', \
                        current_branch() + "..." + tracking_branch()), std=True, err=True)
    if result.returncode != 0:
        return
    ahead, behind = result.stdout.decode('utf-8').strip().split()
    return int(ahead), int(behind)

@check_in_repository
def status():
    """
    Literally just run git status
    """
    r('git status')

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
    for line in r(('git', 'status', '--porcelain'), throw=True, std=True, err=True).stdout.decode('utf-8').split('\n'):
        line = line.strip('\r\n')
        if not line:
            continue
        results.append(FileStatus.of(line))
    return results
