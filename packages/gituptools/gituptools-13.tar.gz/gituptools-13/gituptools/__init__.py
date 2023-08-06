"""Welcome to Gituptools.

100% standard library helper tool for packaging Python from Gitlab CICD
pipelines.  This package pulls as much metadata from the pipeline as
possible to help fill in the setup command.

"""
__all__ = ('setup', 'Gitlab')

import setuptools

from .gitlab import Gitlab


def setup(**kwargs):
    """Gituptools setup wrapper."""
    if Gitlab: # noqa
        kwargs = {**Gitlab.kwargs, **kwargs}
    if 'packages' not in kwargs:
        kwargs['packages'] = setuptools.find_packages()
    setuptools.setup(**kwargs)
