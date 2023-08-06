"""General unit test module."""

import unittest

import gituptools


class TestGeneral(unittest.TestCase):

    """General unit test cases."""

    def test_Gitlab(self):
        """Make sure we can load static files."""
        self.assertIsInstance(gituptools.Gitlab.GITLAB_CI, str)
        self.assertIsInstance(gituptools.Gitlab.CI, str)
        self.assertTrue(gituptools.Gitlab)
        self.assertIsInstance(gituptools.Gitlab.kwargs, dict)
