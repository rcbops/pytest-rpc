# -*- coding: utf-8 -*-

__version__ = '0.5.0'

# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest
import pkg_resources
from datetime import datetime


# ======================================================================================================================
# Globals
# ======================================================================================================================
ENV_VARS = ['BUILD_URL',
            'BUILD_NUMBER',
            'RE_JOB_ACTION',
            'RE_JOB_IMAGE',
            'RE_JOB_SCENARIO',
            'RE_JOB_BRANCH',
            'RPC_RELEASE',
            'RPC_PRODUCT_RELEASE',
            'OS_ARTIFACT_SHA',
            'PYTHON_ARTIFACT_SHA',
            'APT_ARTIFACT_SHA',
            'REPO_URL']


# ======================================================================================================================
# Functions
# ======================================================================================================================
@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session):
    """Add XML properties group to the 'testsuite' element that captures the values for specified environment variables.

    Args:
        session (_pytest.main.Session): The pytest session object
    """

    if session.config.pluginmanager.hasplugin('junitxml'):
            junit_xml_config = getattr(session.config, '_xml', None)

            if junit_xml_config:
                for env_var in ENV_VARS:
                    junit_xml_config.add_global_property(env_var, os.getenv(env_var, 'Unknown'))


def pytest_collection_modifyitems(items):
    """Add XML properties group to each 'testcase' element that captures the UUID for the pytest mark 'test_id'.

    Args:
        items (list(_pytest.nodes.Item)): List of item objects.
    """

    for item in items:
        marker = item.get_marker('test_id')
        if marker is not None:
            test_id = marker.args[0]
            item.user_properties.append(('test_id', test_id))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Add XML properties group to the 'testcase' element that captures start time in UTC.

    Args:
        item (_pytest.nodes.Item): An item object.
    """
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    item.user_properties.append(('start_time', now))


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    """Add XML properties group to the 'testcase' element that captures start time in UTC.

    Args:
        item (_pytest.nodes.Item): An item object.
    """
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    item.user_properties.append(('end_time', now))


def get_xsd():
    """Retrieve a XSD for validating JUnitXML results produced by this plug-in.

    Returns:
        io.BytesIO: A file like stream object.
    """

    return pkg_resources.resource_stream('pytest_rpc', 'data/molecule_junit.xsd')
