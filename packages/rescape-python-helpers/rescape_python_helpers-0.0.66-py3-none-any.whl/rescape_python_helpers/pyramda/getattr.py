from rescape_python_helpers.pyramda.function.curry import curry
import builtins


getattr = curry(lambda name, o: builtins.getattr(o, name))
