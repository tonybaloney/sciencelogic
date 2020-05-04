#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

import uuid


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests', 'pyyaml'
]

setup(
    name='sciencelogic',
    version='0.6.0',
    description="Client library for sciencelogic EM7",
    long_description=readme + '\n\n' + history,
    author="Anthony Shaw",
    author_email='anthonyshaw@apache.org',
    url='https://github.com/tonybaloney/sciencelogic',
    packages=[
        'sciencelogic',
    ],
    package_dir={'sciencelogic':
                 'sciencelogic'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='sciencelogic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
