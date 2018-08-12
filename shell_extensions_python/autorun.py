"""
Provides utilities to allow for functions that run if you type them into the terminal
"""

class autorun: # pylint: disable=C0103
    """
    Decorate a function with @autorun so that typing in the function name runs the function with no arguments
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    def __repr_proxy__(self):
        """
        Outputs the value of the function, to be displayed
        """
        return self.func()
