#!/usr/bin/env python
import codecs
from setuptools import setup, find_packages

version = '1.0.0'

entry_points = {
}


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.fakestatsd',
    version=version,
    author='Chris Utz',
    author_email='open-source@nextthought.com',
    description=('Testing StatsD client'),
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read('CHANGES.rst')
    ),
    license='Apache',
    keywords='python perfmetrics statsd',
    url='https://github.com/NextThought/nti.fakestatsd/',
    project_urls={
        'Bug Tracker': 'https://github.com/NextThought/nti.fakestatsd/issues',
        'Source Code': 'https://github.com/NextThought/nti.fakestatsd/',
        'Documentation': 'https://ntifakestatsd.readthedocs.io/',
    },
    classifiers=[
        "Development Status :: 7 - Inactive",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'perfmetrics >= 3.0.0',
        'setuptools',
    ],
    extras_require={
        'test': [
            'pyhamcrest',
            'nti.testing',
            'zope.testrunner',
        ],
        'docs': [
            'Sphinx',
            'nti.testing',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    namespace_packages=['nti'],
    entry_points=entry_points,
)
