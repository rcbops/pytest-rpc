# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'create_instance' helper function."""


def test_success(mocker):
    """Verify create_instance completes without raising an error and returns
    None when the OpenStack command returns an exit code of '0'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    server = {'id': 'foo', 'name': 'myserver'}
    cr.rc = 0
    cr.stdout = json.dumps(server)

    data = {
        "instance_name": 'instance_name',
        "from_source": 'image',
        "source_name": 'image_name',
        "flavor": 'flavor',
        "network_name": 'network',
    }

    assert not pytest_rpc.helpers.create_instance(data, myhost)


def test_failure(mocker):
    """Verify create_instance raises an error when the OpenStack command
    returns an exit code of '2'.

    relies on mocked objects from testinfra
    """
    """Verify create_instance raises and AssertionError when server instance
    has failed to be successfully created."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    server = {'id': 'foo', 'name': 'myserver'}
    cr.rc = 2
    cr.stdout = json.dumps(server)

    data = {
        "instance_name": 'instance_name',
        "from_source": 'image',
        "source_name": 'image_name',
        "flavor": 'flavor',
        "network_name": 'network',
    }

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_instance(data, myhost)
