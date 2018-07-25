# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import testinfra.backend.base
import testinfra.host
import json

"""Test cases for the '_resource_in_list' helper function."""


def test_resource_in_list_and_expect_true(mocker):
    """Verify _resource_in_list returns True when given resource is found and
    expected state is set to True."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = \
        json.dumps(
                      [
                          {"Status": "ACTIVE",
                           "Name": "myserver",
                           "Image": "Ubuntu 16.04",
                           "ID": "469a7bdd-ceac-4535-8b37-aa5aa892b0ac",
                           "Flavor": "m1.micro",
                           "Networks": "TEST-VXLAN=192.168.1.7"
                           }
                       ]
                   )
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    assert pytest_rpc.helpers._resource_in_list('server', 'myserver', True,
                                                myhost, 1)


def test_resource_in_list_and_expect_false(mocker):
    """Verify _resource_in_list returns False when given resource is found and
    expected state is set to False."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = \
        json.dumps(
                      [
                          {"Status": "ACTIVE",
                           "Name": "myserver",
                           "Image": "Ubuntu 16.04",
                           "ID": "469a7bdd-ceac-4535-8b37-aa5aa892b0ac",
                           "Flavor": "m1.micro",
                           "Networks": "TEST-VXLAN=192.168.1.7"
                           }
                       ]
                   )
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    assert not pytest_rpc.helpers._resource_in_list('server', 'myserver', False,
                                                    myhost, 1)


def test_resource_not_in_list_and_expect_true(mocker):
    """Verify _resource_in_list returns False when given resource is not found and
    expected state is set to True."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps([])
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    assert not pytest_rpc.helpers._resource_in_list('server', 'myserver', True,
                                                    myhost, 1)


def test_resource_not_in_list_and_expect_false(mocker):
    """Verify _resource_in_list returns True when given resource is not found and
    expected state is set to False."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps([])
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    assert pytest_rpc.helpers._resource_in_list('server', 'myserver', False,
                                                myhost, 1)
