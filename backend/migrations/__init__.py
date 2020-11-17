import importlib
import os
from importlib.machinery import SOURCE_SUFFIXES


def _get_module_names():
    path = os.path.dirname(__file__)
    suffix = SOURCE_SUFFIXES[0]
    return [
        m[: -len(suffix)]  # remove .py
        for m in os.listdir(path)
        if m.endswith(suffix) and not m.startswith("__init__")
    ]


def migrations_iterator():
    module_names = _get_module_names()
    for module_name in module_names:
        importpath = f".{module_name}"
        module = importlib.import_module(importpath, "migrations")
        yield module
