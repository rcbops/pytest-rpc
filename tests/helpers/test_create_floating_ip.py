# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import testinfra.backend.base
import testinfra.host
import json

"""Test cases for the 'create_floating_ip' helper function."""


def test_floating_ip_created(mocker):
    """Verify create_floating_ip completes without raising an error and
    returns the created IP address when the OpenStack command returns an exit
    code of '0'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='network_id')

    network = {'id': 'foo', 'floating_ip_address': '10.0.248.202', 'name': 'mynetwork'}
    cr1.rc = 0
    cr1.stdout = json.dumps(network)

    result = pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)
    assert result == '10.0.248.202'


def test_network_not_found(mocker):
    """Verify create_floating_ip raises an error when the given network is not
    found.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value=None)

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)


def test_floating_ip_failure(mocker):
    """Verify create_floating_ip raises an error when the OpenStack create ip
    operation returns an exit code of '2'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='network_id')

    network = {'id': 'foo', 'floating_ip_address': '10.0.248.202', 'name': 'mynetwork'}
    cr1.rc = 2
    cr1.stdout = json.dumps(network)

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)


def test_floating_ip_returns_invalid_json(mocker):
    """Verify create_floating_ip returns None when the OpenStack create ip
    operation returns invalid json.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='network_id')

    cr1.rc = 0
    cr1.stdout = ''

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)
