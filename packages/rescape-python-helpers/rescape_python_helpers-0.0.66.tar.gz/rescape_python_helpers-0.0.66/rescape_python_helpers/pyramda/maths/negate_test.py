from .negate import negate
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def negate_test():
    assert_equal(negate(5), -5)
