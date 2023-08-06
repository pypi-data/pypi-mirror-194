from rescape_python_helpers.pyramda.function.curry import curry


@curry
def take(n, xs):
    return xs[:n]
