# -*- coding: utf-8 -*-

"""Test cases for the 'delete_instance' helper function."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest
import pytest_rpc.helpers


# ======================================================================================================================
# Tests
# ======================================================================================================================
def test_successful_deletion(mocker):
    """Verify delete_instance returns None when server instance is
    successfully deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', return_value=True)

    assert not pytest_rpc.helpers.delete_instance('myserver', 'host')


@pytest.mark.skipif('SKIP_LONG_RUNNING_TESTS' in os.environ, reason='Impatient developer is impatient')
def test_failed_deletion(mocker):
    """Verify delete_instance raises and AssertionError when server instance
    has failed to be successfully deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', side_effect=AssertionError())

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_instance('myserver', 'host')
