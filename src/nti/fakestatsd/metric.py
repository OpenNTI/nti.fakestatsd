#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

__all__ = [
    'Metric',
    'METRIC_COUNTER_KIND',
    'METRIC_GAUGE_KIND',
    'METRIC_SET_KIND',
    'METRIC_TIMER_KIND',
]

from perfmetrics.testing.observation import Observation as Metric
from perfmetrics.testing import OBSERVATION_KIND_COUNTER as METRIC_COUNTER_KIND
from perfmetrics.testing import OBSERVATION_KIND_GAUGE as METRIC_GAUGE_KIND
from perfmetrics.testing import OBSERVATION_KIND_SET as METRIC_SET_KIND
from perfmetrics.testing import OBSERVATION_KIND_TIMER as METRIC_TIMER_KIND
