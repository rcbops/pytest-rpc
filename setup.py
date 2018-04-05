#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-rpc',
    version='0.3.0',
    author='rcbops',
    author_email='rcb-deploy@lists.rackspace.com',
    maintainer='rcbops',
    maintainer_email='rcb-deploy@lists.rackspace.com',
    license='Apache Software License 2.0',
    url='https://github.com/rcbops/pytest-rpc',
    description='Extend py.test for RPC OpenStack testing.',
    long_description=read('README.rst'),
    py_modules=['pytest_rpc'],
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'rpc = pytest_rpc',
        ],
    },
)
