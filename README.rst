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

.. warning::

   This project is deprecated and unmaintained. Its code has moved
   into ``perfmetrics.testing``.

   The following is for historical information only.

nti.fakestatsd is a testing client for verifying StatsD metrics
emitted by perfmetrics.

It's easy to create a new client for use in testing:

.. code-block:: pycon

  >>> from nti.fakestatsd import FakeStatsDClient
  >>> test_client = FakeStatsDClient()

This client exposes the same public interface as
`perfmetrics.statsd.StatsdClient`. For example we can increment
counters, set gauges, etc:

.. code-block:: pycon

  >>> test_client.incr('request_c')
  >>> test_client.gauge('active_sessions', 320)

Unlike `perfmetrics.statsd.StatsdClient`, `~.FakeStatsDClient` simply
tracks the statsd packets that would be sent. This information is
exposed on our ``test_client`` both as the raw statsd packet, and for
convenience this information is also parsed and exposed as `~.Metric`
objects. For complete details see `~.FakeStatsDClient` and `~.Metric`.

.. code-block:: pycon

  >>> test_client.packets
  ['request_c:1|c', 'active_sessions:320|g']
  >>> test_client.metrics
  [Observation(name='request_c', value='1', kind='c', sampling_rate=None), Observation(name='active_sessions', value='320', kind='g', sampling_rate=None)]

For validating metrics we provide a set of hamcrest matchers for use
in test assertions:

.. code-block:: pycon

  >>> from hamcrest import assert_that
  >>> from hamcrest import contains
  >>> from nti.fakestatsd.matchers import is_metric
  >>> from nti.fakestatsd.matchers import is_gauge

We can use both strings and numbers (or any matcher) for the value:

  >>> assert_that(test_client,
  ...     contains(is_metric('c', 'request_c', '1'),
  ...              is_gauge('active_sessions', 320)))
  >>> assert_that(test_client,
  ...     contains(is_metric('c', 'request_c', '1'),
  ...              is_gauge('active_sessions', '320')))
  >>> from hamcrest import is_
  >>> assert_that(test_client,
  ...     contains(is_metric('c', 'request_c', '1'),
  ...              is_gauge('active_sessions', is_('320'))))

If the matching fails, we get a descriptive error:

  >>> assert_that(test_client,
  ...     contains(is_gauge('request_c', '1'),
  ...              is_gauge('active_sessions', '320')))
  Traceback (most recent call last):
  ...
  AssertionError:
  Expected: a sequence containing [(an instance of Metric and (an object with a property 'kind' matching 'g' and an object with a property 'name' matching 'request_c' and an object with a property 'value' matching '1')), (an instance of Metric and (an object with a property 'kind' matching 'g' and an object with a property 'name' matching 'active_sessions' and an object with a property 'value' matching '320'))]
         but: item 0: was Metric(name='request_c', value='1', kind='c', sampling_rate=None)


For complete details and the changelog, see the `documentation
<http://ntifakestatsd.readthedocs.io/>`_.
