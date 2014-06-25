# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Functional tests for :module:`flocker.common.docker`."""

from ..docker import DockerClient
from ..test.test_docker import make_idockerclient_tests

class IDockerClientTests(make_idockerclient_tests(lambda test_case: DockerClient())):
    """``IDockerClient`` tests for ``DockerClient``."""
