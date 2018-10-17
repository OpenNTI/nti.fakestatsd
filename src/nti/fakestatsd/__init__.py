#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"


from perfmetrics.statsd import StatsdClient

from .client import FakeStatsDClient
from .metric import Metric
