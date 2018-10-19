#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest.core.base_matcher import BaseMatcher

from .metric import METRIC_GAUGE_KIND
from .metric import METRIC_COUNTER_KIND
from .metric import METRIC_TIMER_KIND
from .metric import METRIC_SET_KIND

from .metric import Metric


_marker = object()

_metric_kind_display_name = {
    'c': 'counter',
    'g': 'gauge',
    'ms': 'timer',
    's': 'set'
}

class IsMetric(BaseMatcher):

    def __init__(self, kind=_marker, name=_marker, value=_marker, sampling_rate=_marker):
        self.kind = kind
        self.name = name
        self.value = value
        self.sampling_rate = sampling_rate

    def _matches(self, item):
        if not isinstance(item, Metric):
            return False
        
        for attr in ('kind', 'name', 'value', 'sampling_rate', ):
            match_attr = getattr(self, attr, _marker)
            if match_attr is not _marker:
                try:
                    if not match_attr.matches(getattr(item, attr)):
                        return False
                except AttributeError:
                    if match_attr != getattr(item, attr):
                        return False
        return True

    def describe_to(self, description):
        kind_display_name = _metric_kind_display_name.get(self.kind, 'metric')
        description.append_text(kind_display_name)
        if self.kind is not _marker:
            description.append_text(' type=%s' % self.kind)
        if self.name is not _marker:
            description.append_text(' name=%s' % self.name)
        if self.value is not _marker:
            description.append_text(' value=%s' % self.value)
        if self.sampling_rate is not _marker:
            description.append_text(' sampling_rate=%s' % self.sampling_rate)


def is_metric(kind=_marker, name=_marker, value=_marker, sampling_rate=_marker):
    return IsMetric(kind, name, value, sampling_rate)


def is_counter(name=_marker, value=_marker, sampling_rate=_marker):
    return is_metric(METRIC_COUNTER_KIND, name, value, sampling_rate)


def is_gauge(name=_marker, value=_marker, sampling_rate=_marker):
    return is_metric(METRIC_GAUGE_KIND, name, value, sampling_rate)


def is_timer(name=_marker, value=_marker, sampling_rate=_marker):
    return is_metric(METRIC_TIMER_KIND, name, value, sampling_rate)


def is_set(name=_marker, value=_marker, sampling_rate=_marker):
    return is_metric(METRIC_SET_KIND, name, value, sampling_rate)