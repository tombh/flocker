# Copyright Hybrid Logic Ltd.  See LICENSE file for details.
# -*- test-case-name: flocker.node.test.test_model -*-

"""
Record types for representing deployment models.
"""

from characteristic import attributes


@attributes(["repository", "tag"], defaults=dict(tag=u'latest'))
class DockerImage(object):
    """
    An image that can be used to run an application using Docker.

    :ivar unicode repository: eg ``u"hybridcluster/flocker"``
    :ivar unicode tag: eg ``u"release-14.0"``
    :ivar unicode full_name: A readonly property which combines the repository
        and tag in a format that can be passed to `docker run`.
    """

    @property
    def full_name(self):
        return "{repository}:{tag}".format(
            repository=self.repository, tag=self.tag)

    @classmethod
    def from_string(cls, input):
        """
        Given a Docker image name, return a :class:`DockerImage`.

        :param unicode input: A Docker image name in the format
            ``repository[:tag]``.

        :raises ValueError: If Docker image name is not in a valid format.

        :returns: A ``DockerImage`` instance.
        """
        kwargs = {}
        parts = input.rsplit(u':', 1)
        repository = parts[0]
        if not repository:
            raise ValueError("Docker image names must have format "
                             "'repository[:tag]'. Found '{image_name}'."
                             .format(image_name=input))
        kwargs['repository'] = repository
        if len(parts) == 2:
            kwargs['tag'] = parts[1]
        return cls(**kwargs)


@attributes(["name", "mountpoint"])
class AttachedVolume(object):
    """
    A volume attached to an application to be deployed.

    :ivar unicode name: A short, human-readable identifier for this
        volume. For now this is always the same as the name of the
        application it is attached to (see
        https://github.com/ClusterHQ/flocker/issues/49).

    :ivar FilePath mountpoint: The path within the container where this
        volume should be mounted, or ``None`` if unknown
        (see https://github.com/ClusterHQ/flocker/issues/289).
    """


@attributes(["name", "image", "ports", "volume"],
            defaults=dict(image=None, ports=frozenset(), volume=None))
class Application(object):
    """
    A single `application <http://12factor.net/>`_ to be deployed.

    XXX: The image and ports attributes defaults to `None` until we have a way
    to interrogate geard for the docker images associated with its containers.
    See https://github.com/ClusterHQ/flocker/issues/207

    XXX: Only the name is compared in equality checks. See
    https://github.com/ClusterHQ/flocker/issues/267

    :ivar unicode name: A short, human-readable identifier for this
        application.  For example, ``u"site-example.com"`` or
        ``u"pgsql-payroll"``.

    :ivar DockerImage image: An image that can be used to run this
        containerized application.

    :ivar frozenset ports: A ``frozenset`` of ``Port`` instances that
        should be exposed to the outside world.

    :ivar volume: ``None`` if there is no volume, otherwise an
        ``AttachedVolume`` instance.
    """


@attributes(["hostname", "applications"])
class Node(object):
    """
    A single node on which applications will be managed (deployed,
    reconfigured, destroyed, etc).

    :ivar unicode hostname: The hostname of the node.  This must be a
        resolveable name so that Flocker can connect to the node.  This may be
        a literal IP address instead of a proper hostname.

    :ivar frozenset applications: A ``frozenset`` of ``Application`` instances
        describing the applications which are to run on this ``Node``.
    """


@attributes(["nodes"])
class Deployment(object):
    """
    A ``Deployment`` describes the configuration of a number of applications on
    a number of cooperating nodes.  This might describe the real state of an
    existing deployment or be used to represent a desired future state.

    :ivar frozenset nodes: A ``frozenset`` containing ``Node`` instances
        describing the configuration of each cooperating node.
    """


@attributes(['internal_port', 'external_port'])
class Port(object):
    """
    A record representing the mapping between a port exposed internally by an
    application and the corresponding port exposed to the outside world.

    :ivar int internal_port: The port number exposed by the application.
    :ivar int external_port: The port number exposed to the outside world.
    """


@attributes(
    ["applications_to_start", "applications_to_stop",
     "applications_to_restart", "proxies"],
    defaults=dict(proxies=frozenset(), applications_to_restart=frozenset())
)
class StateChanges(object):
    """
    ``StateChanges`` describes changes necessary to make to the current
    state. This might be because of user-specified configuration changes.

    :ivar set applications_to_start: The applications which must be started.
    :ivar set applications_to_restart: The applications which must be
        restarted.
    :ivar set applications_to_stop: The applications which must be stopped.
    :ivar set proxies: The required full ``set`` of
        :class:`flocker.route.Proxy` routes to application on other
        nodes. Defaults to an empty ``frozenset``.
    """
