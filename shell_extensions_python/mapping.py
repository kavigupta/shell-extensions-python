"""
Get the mapping out of the current `col`/`cols`
"""

def col(idx, typ=lambda x: x):
    """
    Get the idx'th column of the underlying data
    """
    return lambda data: _index(data, (idx, typ))

def cols(*idx_types):
    """
    Get the set of idxs'th column of the underlying data.

    Can specify (idx, typ) to cast the given index to the given type.

    For example,
        cols(0, (2, int)) == lambda x: (x[0], int(x[2]))
    """
    return lambda data: tuple(_index(data, idx_type) for idx_type in idx_types)

def _index(data, idx_type):
    if isinstance(idx_type, tuple):
        idx, typ = idx_type
        return typ(data[idx])
    return data[idx_type]
