# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""Docker Client"""

import os

from twisted.internet.endpoints import ProcessEndpoint, connectProtocol

from .process import _AccumulatingProtocol

class DockerClient(object):
    """
    An API for interacting with Docker.

    Communication with Docker should be done via its API, not with this
    approach, but that depends on unreleased Twisted 14.1:
    https://github.com/hybridlogic/flocker/issues/64
    """
    def command(self, reactor, arguments):
        """Run the ``docker`` command-line tool with the given arguments.

        :param reactor: A ``IReactorProcess`` provider.

        :param arguments: A ``list`` of ``bytes``, command-line arguments to
        ``docker``.

        :return: A :class:`Deferred` firing with the bytes of the result (on
            exit code 0), or errbacking with :class:`CommandFailed` or
            :class:`BadArguments` depending on the exit code (1 or 2).
        """
        endpoint = ProcessEndpoint(reactor, b"docker", [b"docker"] + arguments,
                                   os.environ)
        d = connectProtocol(endpoint, _AccumulatingProtocol())
        d.addCallback(lambda protocol: protocol._result)
        return d
