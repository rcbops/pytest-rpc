# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest

"""Test cases for the 'delete_instance' helper function."""


def test_successful_deletion(mocker):
    """Verify delete_instance returns None when server instance is
    successfully deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', return_value=True)

    assert not pytest_rpc.helpers.delete_instance('myserver', 'host')


def test_failed_deletion(mocker):
    """Verify delete_instance raises and AssertionError when server instance
    has failed to be successfully deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', side_effect=AssertionError())

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_instance('myserver', 'host')
