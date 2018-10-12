#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"


from perfmetrics.statsd import StatsdClient

class AbstractMetric(object):

    def __init__(self, name, value, sampling_rate, kind=None):
        self.name = name
        self.value = value
        self.sampling_rate = sampling_rate

    @property
    def type(self):
        # Backwards compatibility, do not use
        return self.kind

class Gauge(AbstractMetric):
    kind = 'g'


class Counter(AbstractMetric):
    kind = 'c'


class Timer(AbstractMetric):

    def __init__(self, name, value, sampling_rate, kind):
        super(Timer, self).__init__(name, value, sampling_rate)
        self.kind = kind

METRIC_TYPES = {
    b'g': Gauge,
    b'c': Counter,
    b's': Timer,
    b'ms': Timer
}

def _as_metrics(data):
    """
    Parses the statsd data packet to a _list_ of metrics.

    See also: https://github.com/etsy/statsd/blob/master/docs/metric_types.md
    """
    metrics = []

    # Start by splitting newlines. this may be a multi-metric packet
    for metric_data in data.split(b'\n'):
        sampling = None
        name = None
        value = None
        kind = None

        # Metrics take the form of <name>:<value>|<type>(|@<sampling_rate>)
        parts = metric_data.split(b'|')
        if len(parts) > 3:
            raise ValueError('Unexpected metric data %s. Too Many Parts' % metric_data)

        if len(parts) == 3:
            sampling_data = parts.pop(-1)
            if not sampling_data.startswith(b'@'):
                raise ValueError('Expected "@" in sampling data. %s' % metric_data)
            sampling = float(sampling_data[1:])

        kind = parts[1]
        name, value = parts[0].split(b':')

        metrics.append(METRIC_TYPES[kind](name, value, sampling, kind))
    return metrics


class FakeStatsDClient(StatsdClient):
    """
    A mock statsd client that tracks sent statsd metrics in memory
    rather than pushing them over a socket.
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
                _raw.append((data, addr,))
                for m in _as_metrics(data):
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
        Iterates the metrics provided to this statsd client
        """
        for metric, _ in self._metrics:
            yield metric
    iter_metrics = __iter__

    def iter_raw(self):
        """
        Iterates the raw metrics provided to the stats d client.
        """
        for data, _ in self._raw:
            yield data

    @property
    def metrics(self):
        return [m for m in self]

    @property
    def packets(self):
        return [p for p in self.iter_raw()]
