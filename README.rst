==========
pytest-rpc
==========

.. image:: https://travis-ci.org/rcbops/pytest-rpc.svg?branch=master
    :target: https://travis-ci.org/rcbops/pytest-rpc
    :alt: See Build Status on Travis CI

Extend py.test for RPC OpenStack testing.

Quick Start Guide
-----------------

1. You can install "pytest-rpc" via `pip`_ from `PyPI`_ ::

    $ pip install pytest-rpc

2. Or you can install "pytest-rpc" via `pip`_ from disk (assumes you're in the root of the repo)::

    $ pip install -e .

Usage
-----

Once installed the plug-in will automatically be loaded by all ``py.test`` test runs executed in the Python environment
in which the ``pytest-rpc`` was installed.

Features
--------

JUnitXML RPC Specific Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a user executes ``py.test`` tests with the ``--junitxml`` and with this plug-in installed, the resulting XML log file
will contain a test suite properties element. The properties element will contain information gathered about the test
run fetched from the local environment.

Contributing
------------

See `CONTRIBUTING.rst`_ for more details on developing for the "pytest-rpc" project.

Credits
-------

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.

.. _CONTRIBUTING.rst: CONTRIBUTING.rst
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
