"""
Represents the result of a pipeline, which contains a recorded standard output, standard error,
    and exit code. Can be combined in a variety of ways or converted into a boolean success code.
"""
from os import linesep

class PipelineResult:
    """
    Represents the result of executing a pipeline
    """
    def __init__(self, stdout, stderr, returncode):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode
    def __bool__(self):
        return self.returncode == 0
    def __repr__(self):
        return ""
    @staticmethod
    def _process(raw_data, single_line, as_lines, raw):
        if single_line + as_lines + raw > 1:
            raise RuntimeError("Incompatible arguments: only one of `single_line, as_lines, raw` can be true")
        if raw:
            return raw_data
        result = b"".join(raw_data).decode('utf-8')
        if single_line:
            lines = [x for x in result.split(linesep) if x]
            if len(lines) != 1:
                raise RuntimeError("Not exactly one line: %s" % lines)
            result = lines[0]
        elif as_lines:
            result = result.split(linesep)
            if result[-1] == "":
                result.pop()
        return result
    def stdout(self, single_line=False, as_lines=False, raw=False):
        """
        Output the stdout as a string with possible modifications
            single_line: strip away all leading and trailing whitespace, and error if there is more than one line
            as_lines: return a list of lines.
        """
        return self._process(self._stdout, single_line=single_line, as_lines=as_lines, raw=raw)
    def stderr(self, single_line=False, as_lines=False, raw=False):
        """
        Output the stderr. See `PipelineResult.stdout` for details
        """
        return self._process(self._stderr, single_line=single_line, as_lines=as_lines, raw=raw)
    def _combine(self, other, returncode_combiner):
        # pylint: disable=protected-access
        return PipelineResult(self._stdout + other._stdout,
                              self._stderr + other._stderr,
                              returncode_combiner(self.returncode, other.returncode))
    def __or__(self, other):
        """
        r(x) | r(y) to run both x and y and return success if either returned success
        """
        # not (not x or not y)
        return self._combine(other, lambda x, y: x and y)
    def __and__(self, other):
        """
        r(x) & r(y) to run both x and y and return success if both returned success
        """
        # not (not x and not y)
        return self._combine(other, lambda x, y: x or y)
    def __add__(self, other):
        """
        r(x) + r(y) to run both x and y and return success if y returned success. In bash:
            { x; y }
        """
        # not (not x and not y)
        return self._combine(other, lambda x, y: y)
