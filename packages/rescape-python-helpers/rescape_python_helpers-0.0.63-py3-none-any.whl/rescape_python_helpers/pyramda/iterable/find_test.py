from .find import find
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def positive(x):
    return x > 0


def find_nocurry_test():
    assert_equal(find(positive, [-2, -1, 0, 1, 2]), 1)


def find_curry_test():
    assert_equal(find(positive)([-2, -1, 0, 1, 2]), 1)
