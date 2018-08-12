"""
Provides an annotator that you place on a generator, allowing it to be a stream or not depending on arguments
"""

def conditional_stream(fn):
    """
    Annotator you place on a generator. If lazy is passed in to the new function
        it returns a generator, otherwise, it returns a list containing the elements
        of the generator
    """
    def result(*args, lazy=False, **kwargs):
        "The new function"
        if lazy:
            return fn(*args, **kwargs)
        return list(fn(*args, **kwargs))
    return result
