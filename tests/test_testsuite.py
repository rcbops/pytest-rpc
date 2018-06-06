# -*- coding: utf-8 -*-

"""Test cases for the 'pytest_runtestloop' hook function for collecting environment variables"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import os
from pytest_rpc import ENV_VARS
from tests.conftest import run_and_parse, is_sub_dict


# ======================================================================================================================
# Tests
# ======================================================================================================================
def test_no_env_vars_set(testdir, undecorated_test_function, testsuite_attribs_exp):
    """Verify that pytest accepts our fixture without setting any environment variables."""

    # Setup
    testdir.makepyfile(undecorated_test_function.format(test_name='test_pass'))

    junit_xml = run_and_parse(testdir)

    # Test
    assert is_sub_dict(testsuite_attribs_exp, junit_xml.testsuite_attribs)

    for env_var in ENV_VARS:
        assert junit_xml.testsuite_props[env_var] == 'Unknown'


def test_env_vars_set(testdir, undecorated_test_function, testsuite_attribs_exp):
    """Verify that pytest accepts our fixture with all relevant environment variables set."""

    # Setup
    testdir.makepyfile(undecorated_test_function.format(test_name='test_pass'))

    for env in ENV_VARS:
        os.environ[env] = env

    junit_xml = run_and_parse(testdir)

    # Test
    assert is_sub_dict(testsuite_attribs_exp, junit_xml.testsuite_attribs)

    assert junit_xml.testsuite_props == {env: env for env in ENV_VARS}
