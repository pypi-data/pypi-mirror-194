from rescape_python_helpers.pyramda.function.curry import curry


@curry
def lesser(a, b):
    return a if a <= b else b
