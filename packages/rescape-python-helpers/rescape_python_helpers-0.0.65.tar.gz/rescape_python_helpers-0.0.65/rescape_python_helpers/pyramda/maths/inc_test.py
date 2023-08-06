from .inc import inc
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def inc_test():
    assert_equal(inc(5), 6)
