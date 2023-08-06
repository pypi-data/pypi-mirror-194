from .chain import chain
from rescape_python_helpers.pyramda.private.asserts import assert_iterables_equal


def to_two(x):
    return [x, x]


def chain_nocurry_test():
    assert_iterables_equal(chain(to_two, [1, 2, 3]), [1, 1, 2, 2, 3, 3])


def chain_curry_test():
    assert_iterables_equal(chain(to_two)([1, 2, 3]), [1, 1, 2, 2, 3, 3])
