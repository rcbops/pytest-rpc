# -*- coding: utf-8 -*-
# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest


# ======================================================================================================================
# Globals
# ======================================================================================================================
ENV_VARS = ['JENKINS_CONSOLE_LOG_URL',
            'SCENARIO',
            'ACTION',
            'IMAGE',
            'OS_ARTIFACT_SHA',
            'PYTHON_ARTIFACT_SHA',
            'APT_ARTIFACT_SHA',
            'GIT_REPO',
            'GIT_BRANCH']


# ======================================================================================================================
# Functions
# ======================================================================================================================
@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session):
    if session.config.pluginmanager.hasplugin('junitxml'):
            junit_xml_config = getattr(session.config, '_xml', None)

            if junit_xml_config:
                for env_var in ENV_VARS:
                    junit_xml_config.add_global_property(env_var, os.getenv(env_var, 'Unknown'))
