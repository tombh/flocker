# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Functional tests for :module:`flocker.common.docker`."""

from ..docker import DockerClient, UnknownContainer
from ...testtools import random_name

from twisted.trial.unittest import TestCase

class DockerClientCommandTests(TestCase):
    """
    Tests for ``DockerClient.command``.
    """
    def cleanup_container(self, container_id):
        """
        Register a container cleanup function to be run after the test finishes.
        """
        self.addCleanup(DockerClient().remove, container_id, force=True)

    def test_run(self):
        """
        ``DockerClient.command`` can be used to run a container.

        The container is started with the `--rm` argument which deletes the test
        container when it exits.
        """
        client = DockerClient()
        expected_environment_variable = b'%s=%s' % (random_name(),random_name())
        d = client.command([b'run',
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

    def assertShortContainerID(self, full_container_id, short_container_ids):
        for short_container_id in short_container_ids:
            if full_container_id.startswith(short_container_id):
                return

        message = 'docker ps output %r does not include %r.' % (
            short_container_ids, full_container_id)
        self.fail(message)

    def test_ps(self):
        """
        ``DockerClient.command`` can be used to list containers

        Create a container and record its container id to a file. Then run ps to
        check that that container id is listed.
        """
        client = DockerClient()
        cidfile = self.mktemp()
        container_name = self.id() + b'_' + random_name()
        d = client.command([b'run',
                             b'--cidfile=%s' % (cidfile,),
                             b'--name=%s' % (container_name,),
                             b'busybox', b'/bin/true']
        )
        def read_container_id(run_stdout_ignored):
            with open(cidfile) as f:
                container_id = f.read()
            self.cleanup_container(container_id)
            return container_id
        d.addCallback(read_container_id)

        def docker_ps(full_container_id):
            """
            List all container IDs (including exited) and check that the
            recently run container is listed.
            """
            d = client.command([b'ps', b'--all', b'--quiet'])
            def check_container_id(ps_stdout):
                self.assertShortContainerID(
                    full_container_id, ps_stdout.splitlines())
            d.addCallback(check_container_id)
            return d
        d.addCallback(docker_ps)

        return d

    def test_stop(self):
        """
        ``DockerClient.command`` can be used to stop a container.
        """
        client = DockerClient()
        container_name = self.id() + b'_' + random_name()
        running_container = client.command([b'run',
                                             b'--detach',
                                             b'--name=%s' % (container_name,),
                                             b'busybox', b'/bin/sleep', b'10']
        )
        def stop_container(full_container_id):
            """
            Attempt to stop the container and check that the stop command returns the
            container_id of the running container.
            """
            full_container_id = full_container_id.rstrip()
            self.cleanup_container(full_container_id)

            d = client.command([b'stop', full_container_id])
            def check_stopped_container_id(stopped_container_id):
                stopped_container_id = stopped_container_id.rstrip()
                self.assertEqual(full_container_id, stopped_container_id)
            d.addCallback(check_stopped_container_id)
            return d
        running_container.addCallback(stop_container)

        return running_container


class DockerClientInspectTests(TestCase):

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
        client = DockerClient()
        name = random_name()
        d = client.inspect(name)
        def test_exception(failure):
            failure.trap(UnknownContainer)
            self.assertEqual(name, failure.value.container_name)
        d.addBoth(test_exception)
        return d
