from rescape_python_helpers.pyramda.function.curry import curry


map = r_map = curry(lambda f, xs: [f(x) for x in xs])
