from rescape_python_helpers.pyramda.function.curry import curry


@curry
def all_satisfy(p, xs):
    return all(map(p, xs))
