
The shell_extensions_python module is a module to be able to write shell scripts on python and use python as your shell.

It provides a number of commands.

## Drop-in replacements for Shell Utilities

 - `cd`: `cd()` takes you to `~`, `cd(path)` takes you to that relative path, and `cd(num)` takes you back `num` steps in your `cd` history.
 - `ls`: `ls(path='.')` returns a list of the contents of the given path, as a directory, sorted by default. Set `sort_key=None` in the call to not sort the results. Set `full=True` to get full paths with respect to this location
 - `cat(path)`: reads the given file and returns it as a string. `cat(path, 'b')` reads the file as a binary sequence.
 - `write(path, contents)`: writes the given contents to the given file. By default does not overwrite existing files. `write(path, contents, clobber=True)` clobbers existing files, and `write(path, contents, append=True)` overwrites existing files.
 - `pwd()`: gets the current working directory
 - `rm(path)`: removes the given path if its a normal file. If it doesn't exist, it will error. To disable this effect, turn on the `ignore_missing=True` file. If it encounters a directory, it will prompt for whether or not it should be removed. To disable this effect so that it errors when it attempts to remove a directory, set `interactive=False`. To disable this so it removes the directory, set `recursively=True`.
 - `globs(path='.')`: expands the given glob into a list of paths.
 - `glob(path='.')`: does the same as globs, but returns a unique value or errors if none exist.
 - `mkdir(path)`: creates the given folder and all its parents. To error if the folder exists, set `error_if_exists=True`
 - `whoami()`: returns the current user
 - `less(file)`: opens the current file using the system's `ls`
 - `cp(src, dest)`: copies the given file from the source to the destination location

## Running external programs

The basic functions for running external programs is `r`. You can call it in one of two ways, either run it as `r('grep -R hi .')` which results in the string being run with command interpolation, or `r(('grep', '-R', 'hi', '.'))`, which is execve-style.

By default, the standard out and error are printed to the terminal. You can capture them by setting `std=True`, `err=True`.

The return value of the `r` function is a `ShellResult` which can be treated like a boolean value as such: `r('make') and r('make check')`. It also can be queried for the stdout/stderr as such: `r('make').stdout()` or `r('make').stderr()`. Each of these functions can take in a `single_line` parameter, which would provide you with a single line, stripped of newlines. Each of these functions can also take in a `as_lines` which then returns a list of lines instead of a single line.
