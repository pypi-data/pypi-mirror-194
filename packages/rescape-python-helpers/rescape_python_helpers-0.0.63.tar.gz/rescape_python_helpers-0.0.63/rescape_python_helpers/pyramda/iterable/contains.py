from rescape_python_helpers.pyramda.function.curry import curry
from rescape_python_helpers.pyramda.relation.equals import equals
from .any_satisfy import any_satisfy


@curry
def contains(x, xs):
    return any_satisfy(equals(x), xs)
