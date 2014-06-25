# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Tests for :module:`flocker.common.docker`."""

from zope.interface.verify import verifyObject

from twisted.trial.unittest import TestCase

from ..docker import IDockerClient

def make_idockerclient_tests(fixture):
    """
    Create a TestCase for IGearClient.

    :param fixture: A fixture that returns a :class:`IGearClient`
        provider.
    """
    class IDockerClientTests(TestCase):
        """
        Tests for :class:`IDockerClient`.

        These are functional tests if run against a real docker.
        """
        def test_interface(self):
            """The tested object provides :class:`IDockerClient`."""
            client = fixture(self)
            self.assertTrue(verifyObject(IDockerClient, client))

    return IDockerClientTests




