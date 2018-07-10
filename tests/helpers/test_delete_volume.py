# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest

"""Test cases for the 'delete_volume' helper function."""


def test_successful_deletion(mocker):
    """Verify delete_volume returns None when OpenStack volume has been
    successfully deleted."""

    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout
    mocker.patch('pytest_rpc.helpers.asset_not_in_the_list', return_value=True)

    assert not pytest_rpc.helpers.delete_volume('myvolume', myhost)


def test_failed_deletion(mocker):
    """Verify delete_volume raises an AssertionError when OpenStack volume has
    failed to successfully be deleted."""

    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout
    mocker.patch('pytest_rpc.helpers.asset_not_in_the_list',
                 return_value=False)

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_volume('myvolume', myhost)
