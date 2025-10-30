import requests


def access_nested_map(nested_map, path):
    """Access a nested map with a path of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url):
    response = requests.get(url)
    return response.json()

# utils.py

def memoize(fn):
    """Memoization decorator for a method."""
    attr_name = "_memoized_" + fn.__name__

    @property
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
