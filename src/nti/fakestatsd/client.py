#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

__all__ = [
    'FakeStatsDClient'
]


from perfmetrics.testing.client import FakeStatsDClient as _Base

class FakeStatsDClient(_Base):

    @property
    def metrics(self):
        return self.observations
