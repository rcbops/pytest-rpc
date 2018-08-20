# -*- coding: utf-8 -*-

"""Test cases for the 'get_expected_value' helper function."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest
import pytest_rpc.helpers


# ======================================================================================================================
# Tests
# ======================================================================================================================
@pytest.mark.skipif('SKIP_LONG_RUNNING_TESTS' in os.environ, reason='Impatient developer is impatient')
def test_get_expected_value_invalid_json(mocker):
    """Verify get_expected_value returns False when invalid JSON is obtained
    via OpenStack query."""
    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout
    assert not pytest_rpc.helpers.get_expected_value('server', 'bar', 'key',
                                                     'expected_value', myhost,
                                                     1)
