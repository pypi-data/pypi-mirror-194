from .cons import cons
from rescape_python_helpers.pyramda.private.asserts import assert_iterables_equal


def cons_nocurry_test():
    assert_iterables_equal(cons(1, [2, 3]), [1, 2, 3])


def cons_curry_test():
    assert_iterables_equal(cons(1)([2, 3]), [1, 2, 3])
