from rescape_python_helpers.pyramda.function.curry import curry


@curry
def tap(f, v):
    f(v)
    return v
