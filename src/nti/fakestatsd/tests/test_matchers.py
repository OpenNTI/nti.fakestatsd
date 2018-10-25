#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import assert_that
from hamcrest import is_
from hamcrest import is_not
from hamcrest import none

from hamcrest.core.string_description import StringDescription

from ..matchers import is_metric
from ..matchers import is_counter
from ..matchers import is_gauge
from ..matchers import is_set
from ..matchers import is_timer

from ..metric import Metric


class TestIsMetric(unittest.TestCase):

    def setUp(self):
        self.counter = Metric.make('foo:1|c')
        self.timer = Metric.make('foo:100|ms|@0.1')
        self.set = Metric.make('foo:bar|s')
        self.gauge = Metric.make('foo:200|g')

    def test_is_metric(self):
        assert_that(self.counter, is_metric('c'))
        assert_that(self.counter, is_metric('c', 'foo'))
        assert_that(self.counter, is_metric('c', 'foo', '1'))
        assert_that(self.counter, is_metric('c', 'foo', '1', None))

    def test_non_metric(self):
        assert_that(object(), is_not(is_metric()))

    def test_is_counter(self):
        assert_that(self.counter, is_counter())

    def test_is_gauge(self):
        assert_that(self.gauge, is_gauge())

    def test_is_set(self):
        assert_that(self.set, is_set())

    def test_is_timer(self):
        assert_that(self.timer, is_timer())

    def test_bad_kind(self):
        assert_that(self.counter, is_not(is_timer()))

    def test_bad_name(self):
        assert_that(self.counter, is_not(is_counter('bar')))

    def test_bad_value(self):
        assert_that(self.counter, is_not(is_counter('foo', '2')))

    def test_bad_sampling(self):
        assert_that(self.timer, is_not(is_counter('foo', '100', None)))

    def test_failure_error(self):
        desc = StringDescription()
        matcher = is_counter('foo', '1', 0.1)
        matcher.describe_to(desc)
        assert_that(str(desc), is_('Metric of form <foo:1|c|@0.1>'))

    def test_components_can_be_matchers(self):
        assert_that(self.counter, is_metric('c', 'foo', '1', none()))
        assert_that(self.timer, is_not(is_metric('ms', 'foo', '100', none())))
        
