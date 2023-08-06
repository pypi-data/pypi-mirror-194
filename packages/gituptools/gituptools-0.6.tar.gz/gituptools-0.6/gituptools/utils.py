"""Gituptools utilities module."""
__all__ = ('attribution',)

import functools
import os
import typing

# --------------------------------------------------------------------------- #

FOLDER: str = os.path.abspath(os.path.dirname(__file__))
STATIC: str = os.path.join(FOLDER, 'static')

klass = typing.Optional[type]
file_name = typing.Optional[str]
kallable = typing.Union[type, typing.Callable]

# --------------------------------------------------------------------------- #


@functools.lru_cache(maxsize=1)
def load_variable_file(fh: str) -> list[str]:
    """Load and split a variable file into a list of slugs."""
    file: str = f'vars.{fh!s}.txt'
    with open(os.path.join(STATIC, file), mode='r') as f:
        return f.read().strip().splitlines()


def attribution(cls: klass = None, file: file_name = None) -> kallable:
    """Attribute all variables in a file to a class."""
    if callable(cls) and file:
        for var in load_variable_file(file):
            setattr(cls, var, os.getenv(var))
        return cls
    return functools.partial(attribution, file=file)
