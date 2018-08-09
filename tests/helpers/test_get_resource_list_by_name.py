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


def test_get_resource_list_by_name_with_data(mocker):
    """Verify get_resource_list_by_name returns a valid json list."""

    data = """[{
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "affd0981-bf11-4472-989c-03c7837a52fb",
               "Name": "delme"
             },
             {
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "b93155f7-770a-4a3a-baef-d8f466a2aa6e",
               "Name": "post-deploy-volume"
             }]"""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps(json.loads(data))
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    volumes = pytest_rpc.helpers.get_resource_list_by_name('volume', myhost)
    assert volumes
    assert '-f json' in myhost.run.call_args[0][0]
    assert 'delme' in [x['Name'] for x in volumes]
