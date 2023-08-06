from rescape_python_helpers.pyramda.function import curry
from rescape_python_helpers.pyramda.iterable import map


@curry
def map_dict(f, dict):
    f_dict = {}
    for k, v in dict.items():
        f_dict[k] = f(v)
    return f_dict
