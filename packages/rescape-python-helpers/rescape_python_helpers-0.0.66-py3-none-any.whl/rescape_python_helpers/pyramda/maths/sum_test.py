from .sum import sum
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def sum_test():
    assert_equal(sum([1, 2, 3]), 6)
