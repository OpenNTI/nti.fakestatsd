================
 nti.fakestatsd
================

.. image:: https://img.shields.io/pypi/v/nti.fakestatsd.svg
        :target: https://pypi.org/project/nti.fakestatsd/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/nti.fakestatsd.svg
        :target: https://pypi.org/project/nti.fakestatsd/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/NextThought/nti.fakestatsd.svg?branch=master
        :target: https://travis-ci.org/NextThought/nti.fakestatsd

.. image:: https://coveralls.io/repos/github/NextThought/nti.fakestatsd/badge.svg
        :target: https://coveralls.io/github/NextThought/nti.fakestatsd

.. image:: http://readthedocs.org/projects/ntifakestatsd/badge/?version=latest
        :target: http://ntifakestatsd.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

nti.fakestatsd is a testing client for verifying StatsD metrics emitted by perfmetrics.

It's easy to create a new client for use in testing.

.. code-block:: bash
   
  >>> from nti.fakestatsd.client import FakeStatsDClient
  >>> test_client = FakeStatsDClient()

This client exposes the same public interface as `perfmetrics.statsd.StatsdClient`. For example we can
increment counters, set gauges, etc.

.. code-block:: bash

  >>> test_client.incr('request_c')
  >>> test_client.gauge('active_sessions', 320)

Unlike `perfmetrics.statsd.StatsdClient`, `FakeStatsDClient` simply tracks the statsd packets that would
be sent. This information is exposed on our ``test_client`` both as the raw statsd packet, and for conveninece this
information is also parsed and exposed as `Metric` objects.  For complete details see `FakeStatsDClient` and `Metric`.

.. code-block:: bash

  >>> test_client.packets
  ['request_c:1|c', 'active_sessions:320|g']
  >>> test_client.metrics
  [<nti.fakestatsd.metric.Metric object at 0x1088c3090>, <nti.fakestatsd.metric.Metric object at 0x1088c3310>]

For validating metrics we provide a set of hamcrest matchers for use in test assertions.

.. code-block:: bash

  >>> from hamcrest import assert_that
  >>> from hamcrest import contains
  >>> from nti.fakestatsd.matchers import is_metric
  >>> from nti.fakestatsd.matchers import is_gauge
  >>> assert_that(test_client, contains(is_metric('c', 'request_c', '1'), is_gauge('active_sessions', '320')))
  >>> assert_that(test_client, contains(is_gauge('request_c', '1'), is_gauge('active_sessions', '320')))
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "VirtualEnvs/fakestatsd/lib/python2.7/site-packages/hamcrest/core/assert_that.py", line 43, in assert_that
      _assert_match(actual=arg1, matcher=arg2, reason=arg3)
    File "VirtualEnvs/fakestatsd/lib/python2.7/site-packages/hamcrest/core/assert_that.py", line 57, in _assert_match
      raise AssertionError(description)
  AssertionError: 
  Expected: a sequence containing [Metric of form <request_c:1|g>, Metric of form <active_sessions:320|g>]
       but: item 0: was <request_c:1|c>


For complete details and the changelog, see the `documentation <http://ntifakestatsd.readthedocs.io/>`_.
