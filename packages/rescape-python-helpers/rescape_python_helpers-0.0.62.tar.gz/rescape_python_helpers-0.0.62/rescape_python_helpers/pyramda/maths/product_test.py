from .product import product
from rescape_python_helpers.pyramda.private.asserts import assert_equal


def product_test():
    assert_equal(product([2, 3, 5]), 30)
