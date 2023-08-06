"""Gitlab specific metadata gathering logic."""
__all__ = ('Gitlab',)

import os
import typing

from . import utils

# --------------------------------------------------------------------------- #


class EnvAttrs(type):

    """Route attributes to the environment."""

    def __getattr__(self, attr: str) -> typing.Union[str, None]:
        """Reroute attributes to the environment."""
        return os.getenv(attr)

    def __bool__(self) -> bool:
        """Is this a Gitlab CICD pipeline runtime?"""
        return self.GITLAB_CI is not None

    @property
    def kwargs(cls) -> dict:
        """Extract Gitlab CI variables into kwargs for setuptools.setup()."""
        return {
            'author': cls.CI_COMMIT_AUTHOR,
            'name': cls.CI_PROJECT_NAME,
            'url': cls.CI_PROJECT_URL,
            'project_urls': {
                'Documentation': cls.CI_PAGES_URL,
                'Source': cls.CI_PROJECT_URL
                }
            }


@utils.attribution(file='gitlab')
class Gitlab(metaclass=EnvAttrs):

    """Helper class to access Gitlab environment vars."""

    pass
