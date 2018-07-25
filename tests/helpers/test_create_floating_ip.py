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
    cr2 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=[cr1, cr2, cr2])

    network = {'id': 'foo', 'name': 'mynetwork'}
    ip_address = {'name': '192.168.1.1'}
    cr1.rc = cr2.rc = 0
    cr1.stdout = json.dumps(network)
    cr2.stdout = json.dumps(ip_address)

    result = pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)
    assert result == ip_address['name']


def test_network_not_found(mocker):
    """Verify create_floating_ip raises an error when the given network is not
    found.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    cr.rc = 1
    cr.stdout = ''

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
    cr2 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=[cr1, cr2, cr2])

    network = {'id': 'foo', 'name': 'mynetwork'}
    cr1.rc = 0
    cr1.stdout = json.dumps(network)
    cr2.rc = 2
    cr2.stdout = ''

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
    cr2 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=[cr1, cr2, cr2])

    network = {'id': 'foo', 'name': 'mynetwork'}
    cr1.rc = cr2.rc = 0
    cr1.stdout = json.dumps(network)
    cr2.rc = 0
    cr2.stdout = ''

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_floating_ip('mynetwork', myhost)
