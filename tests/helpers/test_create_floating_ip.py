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
    ip_address = """{
        "router_id": null,
        "status": "DOWN",
        "description": "",
        "created_at": "2018-08-16T18:27:05Z",
        "updated_at": "2018-08-16T18:27:05Z",
        "floating_network_id": "59f88fdd-293d-429e-9f2a-6af665e0aee5",
        "fixed_ip_address": null,
        "floating_ip_address": "10.0.248.202",
        "revision_number": 0,
        "project_id": "ca37d49d3231475ba0d17d9efc043e09",
        "port_id": null,
        "id": "f6096508-9a38-43bc-ab27-607511ee34dd",
        "name": "10.0.248.202"
    }"""
    cr1.rc = cr2.rc = 0
    cr1.stdout = json.dumps(network)
    cr2.stdout = json.dumps(json.loads(ip_address))

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
