# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the '_asset_in_list' helper function."""


def test_asset_in_list_and_expect_true(mocker):
    """Verify _asset_in_list returns True when given asset is found and
    expected state is set to True."""

    os_list = 'myserver'
    mocker.patch('pytest_rpc.helpers.openstack_name_list',
                 return_value=os_list)

    assert pytest_rpc.helpers._asset_in_list('server', 'myserver', True,
                                             'host', 1)


def test_asset_in_list_and_expect_false(mocker):
    """Verify _asset_in_list returns False when given asset is found and
    expected state is set to False."""

    os_list = 'myserver'
    mocker.patch('pytest_rpc.helpers.openstack_name_list',
                 return_value=os_list)

    assert not pytest_rpc.helpers._asset_in_list('server', 'myserver', False,
                                                 'host', 1)


def test_asset_not_in_list_and_expect_true(mocker):
    """Verify _asset_in_list returns False when given asset is not found and
    expected state is set to True."""

    os_list = ''
    mocker.patch('pytest_rpc.helpers.openstack_name_list',
                 return_value=os_list)

    assert not pytest_rpc.helpers._asset_in_list('server', 'myserver', True,
                                                 'host', 1)


def test_asset_not_in_list_and_expect_false(mocker):
    """Verify _asset_in_list returns True when given asset is not found and
    expected state is set to False."""

    os_list = ''
    mocker.patch('pytest_rpc.helpers.openstack_name_list',
                 return_value=os_list)

    assert pytest_rpc.helpers._asset_in_list('server', 'myserver', False,
                                             'host', 1)
