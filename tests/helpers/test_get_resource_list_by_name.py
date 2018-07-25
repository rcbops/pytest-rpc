# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'get_resource_list_by_name' helper function."""


def test_get_resource_list_by_name(mocker):
    """Verify get_resource_list_by_name returns a valid json list."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps([])
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    assert type(pytest_rpc.helpers.get_resource_list_by_name('server', myhost)) == list
