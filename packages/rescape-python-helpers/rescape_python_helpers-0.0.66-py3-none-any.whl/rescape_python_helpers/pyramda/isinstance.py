from rescape_python_helpers.pyramda.function.curry import curry
import builtins


isinstance = curry(lambda type, v: builtins.isinstance(v, type))
