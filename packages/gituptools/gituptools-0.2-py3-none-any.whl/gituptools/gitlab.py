"""Gitlab specific metadata gathering logic."""
__all__ = ('Gitlab',)

import os
import typing

# --------------------------------------------------------------------------- #


class EnvAttrs(type):

    """Route attributes to the environment."""

    def __getattr__(self, key: str) -> typing.Optional[str]:
        """Pull value from environment."""
        return os.getenv(key)

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


class Gitlab(metaclass=EnvAttrs):

    """Helper class to access Gitlab environment vars."""

    pass
