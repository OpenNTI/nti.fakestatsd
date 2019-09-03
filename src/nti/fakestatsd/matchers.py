#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

__all__ = [
    'is_metric',
    'is_counter',
    'is_gauge',
    'is_set',
    'is_timer',
]

from perfmetrics.testing.matchers import is_observation as is_metric
from perfmetrics.testing.matchers import is_counter
from perfmetrics.testing.matchers import is_set
from perfmetrics.testing.matchers import is_gauge
from perfmetrics.testing.matchers import is_timer
