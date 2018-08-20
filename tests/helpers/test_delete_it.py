# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import testinfra.backend.base
import testinfra.host
import json

"""Test cases for the 'delete_it' helper function."""


def test_success(mocker):
    """Verify delete_it completes without raising an error and returns None
    when the OpenStack command returns an exit code of '0'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', side_effect=['server_id',
                 None])

    server = {'id': 'server_id', 'name': 'myserver'}
    cr1.rc = 0
    cr1.stdout = json.dumps(server)

    assert not pytest_rpc.helpers.delete_it('server', 'myserver', myhost)


def test_failure(mocker):
    """Verify delete_it raises an error when the OpenStack command returns an
    exit code of '2'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='server_id')

    cr1.rc = 2
    cr1.stdout = ''

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_it('server', 'myserver', myhost)


def test_resource_not_deleted(mocker):
    """Verify delete_it raises an error when the OpenStack resource is not
    deleted.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='server_id')

    server = {'id': 'server_id', 'name': 'myserver'}
    cr1.rc = 0
    cr1.stdout = json.dumps(server)

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_it('server', 'myserver', myhost)
