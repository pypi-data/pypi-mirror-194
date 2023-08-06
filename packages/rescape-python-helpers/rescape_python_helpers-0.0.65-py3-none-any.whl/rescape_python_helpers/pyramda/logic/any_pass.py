from rescape_python_helpers.pyramda.function.curry import curry
from rescape_python_helpers.pyramda.function.always import always
from rescape_python_helpers.pyramda.iterable.reduce import reduce
from .either import either


@curry
def any_pass(ps, v):
    return reduce(either, always(False), ps)(v)
