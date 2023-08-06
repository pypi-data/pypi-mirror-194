from rescape_python_helpers.pyramda.function.curry import curry


@curry
def complement(p, v):
    return not p(v)
