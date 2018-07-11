# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'asset_not_in_the_list' helper function."""


def test_true(mocker):
    """Verify asset_not_in_the_list returns True when _asset_in_list resolves
    to True."""

    mocker.patch('pytest_rpc.helpers._asset_in_list', return_value=True)

    assert pytest_rpc.helpers.asset_not_in_the_list('server', 'myserver',
                                                    'host')


def test_false(mocker):
    """Verify asset_not_in_the_list returns False when _asset_in_list resolves
    to False."""

    mocker.patch('pytest_rpc.helpers._asset_in_list', return_value=False)

    assert not pytest_rpc.helpers.asset_not_in_the_list('server', 'myserver',
                                                        'host')
