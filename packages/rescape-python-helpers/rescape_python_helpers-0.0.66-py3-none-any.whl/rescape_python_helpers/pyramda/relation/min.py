from rescape_python_helpers.pyramda.function.curry import curry
import builtins


@curry
def min(xs):
    return builtins.min(xs)
