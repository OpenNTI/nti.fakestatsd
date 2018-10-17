#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import functools

import unittest

from hamcrest import none
from hamcrest import assert_that
from hamcrest import contains
from hamcrest import is_
from hamcrest import has_length
from hamcrest import has_property
from hamcrest import calling
from hamcrest import raises

from ..metric import Metric
from ..metric import METRIC_COUNTER_KIND
from ..metric import METRIC_GAUGE_KIND
from ..metric import METRIC_SET_KIND
from ..metric import METRIC_TIMER_KIND


class TestMetricParsing(unittest.TestCase):

    def test_invalid_packet(self):
        packet = 'junk'
        assert_that(calling(functools.partial(Metric.make_all, packet)),
                    raises(ValueError))

        packet = 'foo|bar|baz|junk'
        assert_that(calling(functools.partial(Metric.make_all, packet)),
                    raises(ValueError))

        packet = 'gorets:1|c|0.1'
        assert_that(calling(functools.partial(Metric.make_all, packet)),
                    raises(ValueError))

    def test_counter(self):
        packet = 'gorets:1|c'
        metric = Metric.make_all(packet)

        assert_that(metric, has_length(1))
        metric = metric[0]

        assert_that(metric.kind, is_(METRIC_COUNTER_KIND))
        assert_that(metric.name, is_('gorets'))
        assert_that(metric.value, is_('1'))
        assert_that(metric.sampling_rate, is_(none()))

    def test_sampled_counter(self):
        packet = 'gorets:1|c|@0.1'
        metric = Metric.make_all(packet)

        assert_that(metric, has_length(1))
        metric = metric[0]

        assert_that(metric.kind, is_(METRIC_COUNTER_KIND))
        assert_that(metric.name, is_('gorets'))
        assert_that(metric.value, is_('1'))
        assert_that(metric.sampling_rate, is_(0.1))

    def test_timer(self):
        packet = 'glork:320|ms'
        metric = Metric.make_all(packet)

        assert_that(metric, has_length(1))
        metric = metric[0]

        assert_that(metric.kind, is_(METRIC_TIMER_KIND))
        assert_that(metric.name, is_('glork'))
        assert_that(metric.value, is_('320'))
        assert_that(metric.kind, is_('ms'))
        assert_that(metric.sampling_rate, is_(none()))

    def test_set(self):
        packet = 'glork:3|s'
        metric = Metric.make_all(packet)

        assert_that(metric, has_length(1))
        metric = metric[0]

        assert_that(metric.kind, is_(METRIC_SET_KIND))
        assert_that(metric.name, is_('glork'))
        assert_that(metric.value, is_('3'))
        assert_that(metric.kind, is_('s'))
        assert_that(metric.sampling_rate, is_(none()))

    def test_guage(self):
        packet = 'gaugor:+333|g'
        metric = Metric.make_all(packet)

        assert_that(metric, has_length(1))
        metric = metric[0]

        assert_that(metric.kind, is_(METRIC_GAUGE_KIND))
        assert_that(metric.name, is_('gaugor'))
        assert_that(metric.value, is_('+333'))
        assert_that(metric.sampling_rate, is_(none()))

    def test_multi_metric(self):
        packet = 'gorets:1|c\nglork:320|ms\ngaugor:333|g\nuniques:765|s'
        metrics = Metric.make_all(packet)
        assert_that(metrics, contains(has_property('kind', METRIC_COUNTER_KIND),
                                      has_property('kind', METRIC_TIMER_KIND),
                                      has_property('kind', METRIC_GAUGE_KIND),
                                      has_property('kind', METRIC_SET_KIND)))

    def test_metric_string(self):
        metric = Metric.make('gaugor:+333|g')
        assert_that(str(metric), is_('gaugor:+333|g'))

        packet = 'gorets:1|c|@0.1'
        metric = Metric.make_all(packet)[0]
        metric = Metric.make_all(str(metric))[0]

        assert_that(metric.kind, is_(METRIC_COUNTER_KIND))
        assert_that(metric.name, is_('gorets'))
        assert_that(metric.value, is_('1'))
        assert_that(metric.sampling_rate, is_(0.1))

    def test_factory(self):
        metric = Metric.make('gaugor:+333|g')
        assert_that(str(metric), is_('gaugor:+333|g'))

        assert_that(calling(functools.partial(Metric.make, 'gaugor:+333|g\ngaugor:+333|g')),
                    raises(ValueError))
        
