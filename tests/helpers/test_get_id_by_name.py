# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'get_id_by_name' helper function."""


def test_successful_query(mocker):
    """Verify get_id_by_name returns ID value when OpenStack query is
    successful."""

    data = """[{
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "myvolume-uuid",
               "Name": "myvolume"
             },
             {
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "extra-volume-uuid",
               "Name": "extra volume"
             }]"""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps(json.loads(data))
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    result = pytest_rpc.helpers.get_id_by_name('volume', 'myvolume', myhost)
    assert result == 'myvolume-uuid'


def test_invalid_json(mocker):
    """Verify get_id_by_name returns None when OpenStack query returns invalid
    JSON."""

    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout

    result = pytest_rpc.helpers.get_id_by_name('server', 'myserver', myhost)
    assert result is None


def test_no_id(mocker):
    """Verify get_id_by_name returns None when OpenStack query returns JSON
    without an id value."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.stdout = json.dumps([{'foo': 'bar'}])
    mocker.patch('testinfra.host.Host.run', return_value=command_result)
    result = pytest_rpc.helpers.get_id_by_name('server', 'myserver', myhost)

    assert result is None


def test_multiple_resources_with_same_name(mocker):
    """Verify get_id_by_name returns ID value of a found resource  when OpenStack query
    returns multiple resources."""

    data = """[{
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "myvolume-first-uuid",
               "Name": "myvolume"
             },
             {
               "Status": "available",
               "Size": 1,
               "Attached to": "",
               "ID": "myvolume-second-uuid",
               "Name": "myvolume"
             }]"""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps(json.loads(data))
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    result = pytest_rpc.helpers.get_id_by_name('volume', 'myvolume', myhost)
    assert result == 'myvolume-first-uuid'
