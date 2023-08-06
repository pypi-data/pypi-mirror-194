from .multiply import multiply
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def multiply_nocurry_test():
    assert_equal(multiply(3, 6), 18)


def multiply_curry_test():
    assert_equal(multiply(3)(6), 18)
