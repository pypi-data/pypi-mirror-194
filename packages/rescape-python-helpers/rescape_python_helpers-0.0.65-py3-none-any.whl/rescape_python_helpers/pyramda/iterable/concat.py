from rescape_python_helpers.pyramda.function.curry import curry


@curry
def concat(xs, ys):
    return xs + ys
