# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'openstack_name_list' helper function."""


def test_openstack_name_list(mocker):
    """Verify openstack_name_list returns string."""

    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout
    assert type(pytest_rpc.helpers.openstack_name_list('server', myhost)) == str
