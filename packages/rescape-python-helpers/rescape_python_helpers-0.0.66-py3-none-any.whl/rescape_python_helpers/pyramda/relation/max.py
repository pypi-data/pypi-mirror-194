from rescape_python_helpers.pyramda.function.curry import curry
import builtins


@curry
def max(xs):
    return builtins.max(xs)
