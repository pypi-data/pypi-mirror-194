from rescape_python_helpers.pyramda.function.curry import curry


@curry
def drop(n, xs):
    return xs[n::]
