==========
pytest-rpc
==========

.. image:: https://travis-ci.org/rcbops/pytest-rpc.svg?branch=master
    :target: https://travis-ci.org/rcbops/pytest-rpc
    :alt: See Build Status on Travis CI

Extend py.test for RPC OpenStack testing.

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

JUnitXML RPC Specific Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a user executes ``py.test`` tests with the ``--junitxml`` and with this plug-in installed, the resulting XML log file
will contain a test suite properties element. The properties element will contain information gathered about the test
run fetched from the local environment.


Installation
------------

You can install "pytest-rpc" via `pip`_ from `PyPI`_::

    $ pip install pytest-rpc


Usage
-----

Once installed the plug-ing will automatically be loaded by all ``py.test`` test runs.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

You can install dependencies via the ``requirements.txt`` file using `pip`_ from `PyPI`_::

    $ pip install -r requirements.txt

License
-------

Distributed under the terms of the `Apache Software License 2.0`_ license, "pytest-rpc" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/rcbops/pytest-rpc/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
