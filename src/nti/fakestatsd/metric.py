#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"


METRIC_GAUGE_KIND = 'g'
METRIC_COUNTER_KIND = 'c'
METRIC_SET_KIND = 's'
METRIC_TIMER_KIND = 'ms'


def _parse_sampling_data(data):
    if not data.startswith('@'):
        raise ValueError('Expected "@" in sampling data. %s' % data)
    return float(data[1:])

def _as_metric(metric_data):
    """
    Parses a single metric packet in to `Metric`.
    
    Metrics take the form of <name>:<value>|<type>(|@<sampling_rate>)

    A ValueError is raised for invalid data
    """

    sampling = None
    name = None
    value = None
    kind = None
    parts = metric_data.split('|')
    if len(parts) < 2 or len(parts) > 3:
        raise ValueError('Unexpected metric data %s. Wrong number of parts' % metric_data)

    if len(parts) == 3:
        sampling_data = parts.pop(-1)
        sampling = _parse_sampling_data(sampling_data)

    kind = parts[1]
    name, value = parts[0].split(':')

    return Metric(name, value, kind, sampling_rate=sampling)

def _as_metrics(data):
    """
    Parses the statsd data packet to a _list_ of metrics.

    See also: https://github.com/etsy/statsd/blob/master/docs/metric_types.md
    """
    metrics = []

    # Multi metric packets are seperated by newlines
    for metric_data in data.split('\n'):
        metrics.append(_as_metric(metric_data))
    return metrics


class Metric(object):
    """
    The representation of a single statsd metric.

    Attributes:
        name (str): The metric name
        value (str): The value provided for the metric
        kind (str): The statsd code for the type of metric. e.g. (g, c, s, ms)
        sampling_rate: (number, optional): The rate with which this event has been
            sampled from.
    """

    def __init__(self, name, value, kind, sampling_rate=None):
        self.name = name
        self.value = value
        self.sampling_rate = sampling_rate
        self.kind = kind

    @classmethod
    def make(cls, packet):
        """
        Creates a metric from the provided statsd packet.
        Raises a ValueError if packet is a multi metric packet
        """
        metrics = cls.make_all(packet)
        if len(metrics) != 1:
            raise ValueError('Must supply a single metric packet. %s supplied' % packet)
        return metrics[0]

    @classmethod
    def make_all(cls, packet):
        """
        Makes a list of metrics from the provided statsd packet.
        Like `make` but supports multi metric packets
        """
        return _as_metrics(packet)

    def __str__(self):
        sampling_string = '|@%f' % self.sampling_rate if self.sampling_rate is not None else ''
        return '%s:%s|%s%s' % (self.name, self.value, self.kind, sampling_string)
