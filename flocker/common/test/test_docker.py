# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Tests for :module:`flocker.common.docker`."""

from zope.interface.verify import verifyObject

from twisted.trial.unittest import TestCase

from ...testtools import random_name, WithInitTestsMixin
from ..docker import IDockerClient, UnknownContainer

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


        def test_inspect(self):
            """
            ``IDockerClient.inspect`` returns a deferred that fires with the
            configuration of the named container as a nest dictionary.
            """


        def test_inspect_unknown_container(self):
            """
            ``IDockerClient.inspect`` raises ``UnknownContainer`` if the named
            container does not exist.
            """
            client = fixture(self)
            name = random_name()
            d = client.inspect(name)
            def test_exception(failure):
                failure.trap(UnknownContainer)
                self.assertEqual(name, failure.value.container_name)
            d.addBoth(test_exception)
            return d

    return IDockerClientTests



class UnknownContainerTests(WithInitTestsMixin, TestCase):
    record_type = UnknownContainer
    values = dict(container_name=b'busybox-app')
