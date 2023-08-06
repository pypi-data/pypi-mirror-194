from rescape_python_helpers.pyramda.function.curry import curry
from rescape_python_helpers.pyramda.iterable.reduce import reduce
from .multiply import multiply


product = reduce(multiply, 1)
