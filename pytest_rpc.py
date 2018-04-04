# -*- coding: utf-8 -*-
# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest


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
