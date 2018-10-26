#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"


from perfmetrics.statsd import StatsdClient

from .metric import Metric


class FakeStatsDClient(StatsdClient):
    """
    A mock statsd client that tracks sent statsd metrics in memory
    rather than pushing them over a socket. This class is a drop
    in replacement for `perfmetrics.statsd.StatsdClient` that collects statsd
    packets and `~.Metric` that are sent through the client.
    """

    def __init__(self, prefix=''):
        """
        Create a mock statsd client with the given prefix.
        """
        super(FakeStatsDClient, self).__init__(prefix=prefix)

        # Monkey patch the socket to track things in memory instead
        self._raw = _raw = []
        self._metrics = _metrics = []

        class DummySocket(object):
            def sendto(self, data, addr):
                # The client encoded to bytes
                assert isinstance(data, bytes)
                # We always want native strings here, that's what the
                # user specified when calling the StatsdClient methods.
                data = data.decode('utf-8') if bytes is not str else data
                _raw.append((data, addr,))
                for m in Metric.make_all(data):
                    _metrics.append((m, addr,))

        self.udp_sock.close()
        self.udp_sock = DummySocket()

    def clear(self):
        """
        Clears the statsd metrics that have been collected
        """
        del self._raw[:]
        del self._metrics[:]

    def __len__(self):
        """
        The number of metrics sent. This accounts for multi metric packets
        that may be sent.
        """
        return len(self._metrics)

    def __iter__(self):
        """
        Iterates the `Metrics <~.Metric>` provided to this statsd
        client.
        """
        for metric, _ in self._metrics:
            yield metric
    iter_metrics = __iter__

    def iter_raw(self):
        """
        Iterates the raw statsd packets provided to the statsd client.
        """
        for data, _ in self._raw:
            yield data

    @property
    def metrics(self):
        """
        A list of `~.Metric` objects collected by this client.

        .. seealso:: `iter_metrics`
        """
        return [m for m in self]

    @property
    def packets(self):
        """
        A list of raw statsd packets collected by this client.

        .. seealso:: `iter_raw`
        """
        return [p for p in self.iter_raw()]
