from rescape_python_helpers.pyramda.function.curry import curry


@curry
def mean(xs):
    return sum(xs) / len(xs)
