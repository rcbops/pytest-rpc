#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pytest>=3.5.0', 'setuptools']
packages = ['pytest_rpc']
entry_points = {
    'pytest11': [
        'rpc=pytest_rpc',
    ],
}

setup(
    name='pytest-rpc',
    version='0.6.0',
    author='rcbops',
    author_email='rcb-deploy@lists.rackspace.com',
    maintainer='rcbops',
    maintainer_email='rcb-deploy@lists.rackspace.com',
    license='Apache Software License 2.0',
    url='https://github.com/rcbops/pytest-rpc',
    keywords='pytest-rpc',
    description='Extend py.test for RPC OpenStack testing.',
    long_description=readme + '\n\n' + history,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    packages=packages,
    include_package_data=True,
    entry_points=entry_points,
)
