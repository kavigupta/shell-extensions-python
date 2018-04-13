
import pickle

def ploads(filename, limit=float('inf')):
    """
    Loads several pickles.
    """
    pickles = []
    try:
        while True:
            with open(filename, 'rb') as f:
                pickles.append(pickle.load(f))
            if len(pickles) >= limit:
                break
    except EOFError:
        pass
    return pickles

def pload(filename):
    """
    Loads a single pickle from a file
    """
    results = ploads(filename, limit=2)
    if not results:
        raise RuntimeError("No pickle found!")
    elif len(results) > 1:
        raise RuntimeError("Too many pickles!")
    else:
        return results[0]

def psaves(filename, pickles):
    """
    Save several pickles to a file
    """
    with open(filename, 'wb') as f:
        for pick in pickles:
            pickle.dump(f, pick)

def psave(filename, pickl):
    """
    Save a single pickle to a file
    """
    psaves(filename, [pickl])
