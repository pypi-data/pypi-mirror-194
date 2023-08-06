from rescape_python_helpers.pyramda.function.curry import curry
import builtins


@curry
def sum(xs):
    return builtins.sum(xs)
