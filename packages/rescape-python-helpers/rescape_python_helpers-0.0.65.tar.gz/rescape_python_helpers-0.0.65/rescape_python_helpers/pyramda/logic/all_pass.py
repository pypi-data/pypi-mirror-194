from rescape_python_helpers.pyramda.function.curry import curry
from rescape_python_helpers.pyramda.function.always import always
from rescape_python_helpers.pyramda.iterable.reduce import reduce
from .both import both


@curry
def all_pass(ps, v):
    return reduce(both, always(True), ps)(v)
