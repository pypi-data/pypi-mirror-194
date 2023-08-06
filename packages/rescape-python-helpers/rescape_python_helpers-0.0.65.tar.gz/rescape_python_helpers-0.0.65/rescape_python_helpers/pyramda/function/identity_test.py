from .identity import identity
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def identity_test():
    assert_equal(identity(3), 3)
