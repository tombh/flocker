# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Functional tests for :module:`flocker.common.docker`."""

from ..docker import DockerClient
from ...testtools import random_name
from ..test.test_docker import make_idockerclient_tests

from twisted.trial.unittest import TestCase

class IDockerClientTests(make_idockerclient_tests(lambda test_case: DockerClient())):
    """``IDockerClient`` tests for ``DockerClient``."""


class DockerClientTests(TestCase):
    """
    Tests for implementation specific parts of ``DockerClient``.
    """
    def test_command_run(self):
        """
        ``DockerClient._command`` can be used to run a container.
        """
        client = DockerClient()
        expected_environment_variable = b'%s=%s' % (random_name(),random_name())
        d = client._command([b'run',
                             b'--rm',
                             b'--env=%s' % (expected_environment_variable,),
                             b'busybox', b'/usr/bin/env']
        )

        def read_cidfile(stdout):
            self.assertIn(expected_environment_variable, stdout.splitlines())

        d.addCallback(read_cidfile)

        return d
