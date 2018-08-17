# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest

"""Test cases for the 'delete_volume' helper function."""


def test_successful_deletion(mocker):
    """Verify delete_volume returns None when OpenStack volume has been
    successfully deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', return_value=True)

    assert not pytest_rpc.helpers.delete_volume('myvolume', 'host')


def test_failed_deletion(mocker):
    """Verify delete_volume raises an AssertionError when OpenStack volume has
    failed to successfully be deleted."""

    mocker.patch('pytest_rpc.helpers.delete_it', side_effect=AssertionError())

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_volume('myvolume', 'host')
