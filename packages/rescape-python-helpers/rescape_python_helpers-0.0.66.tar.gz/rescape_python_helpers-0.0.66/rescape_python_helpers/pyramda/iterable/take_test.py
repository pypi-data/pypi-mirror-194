from .take import take
from rescape_python_helpers.pyramda.private.asserts import assert_iterables_equal


def take_nocurry_test():
    assert_iterables_equal(take(2, [1, 2, 3, 4]), [1, 2])


def take_curry_test():
    assert_iterables_equal(take(2)([1, 2, 3, 4]), [1, 2])
