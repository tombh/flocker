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

        The container is started with the `--rm` argument which deletes the test
        container when it exits.
        """
        client = DockerClient()
        expected_environment_variable = b'%s=%s' % (random_name(),random_name())
        d = client._command([b'run',
                             b'--rm',
                             b'--env=%s' % (expected_environment_variable,),
                             b'busybox', b'/usr/bin/env']
        )

        def check_environment(stdout):
            """
            The supplied environment variable is printed by the env command
            inside the container.
            """
            self.assertIn(expected_environment_variable, stdout.splitlines())

        d.addCallback(check_environment)

        return d

    def assertRunningContainerID(self, container_id, running_container_ids):
        for short_container_id in running_container_ids:
            if container_id.startswith(short_container_id):
                return

        message = 'docker ps output %r does not include %r.' % (
            running_container_ids, container_id)
        self.fail(message)

    def test_command_ps(self):
        """
        ``DockerClient._command`` can be used to list containers

        Create a container and record its container id to a file. Then run ps to
        check that that container id is listed.
        """
        client = DockerClient()
        d = client._command([b'run',
                             b'--name=%s' % (self.id(),),
                             b'--detach',
                             b'busybox', b'/bin/sleep', b'10']
        )
        def docker_ps(run_stdout):
            """
            docker run prints the container ID to stdout.
            """
            d = client._command([b'ps', b'--quiet'])
            def check_container_id(ps_stdout):
                self.assertRunningContainerID(
                    run_stdout, ps_stdout.splitlines())
            d.addCallback(check_container_id)
            return d
        d.addCallback(docker_ps)

        return d
