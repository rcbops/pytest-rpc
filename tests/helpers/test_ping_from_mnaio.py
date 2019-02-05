# -*- coding: utf-8 -*-
"""Test cases for the 'ping_from_mnaio' helper function."""
# ==============================================================================
# Imports
# ==============================================================================
import pytest_rpc.helpers


# ==============================================================================
# Tests
# ==============================================================================
def test_successful_ping(mocker):
    """Verify that the helper returns "True" when the ping is successful.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
    """

    # Mock
    mocker.patch('pytest_rpc.helpers.call', autospec=True, return_value=0)

    # Test
    assert pytest_rpc.helpers.ping_from_mnaio('fake_host')


def test_unsuccessful_ping(mocker):
    """Verify that the helper returns "False" when the ping fails.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
    """

    # Mock
    mocker.patch('pytest_rpc.helpers.call', autospec=True, return_value=1)

    # Test
    assert pytest_rpc.helpers.ping_from_mnaio('fake_host', 0) is False
