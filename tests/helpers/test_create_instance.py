# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'create_instance' helper function."""


def test_success(mocker):
    """Verify create_instance returns instance id when the OpenStack command
    succeeds.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='id_value')

    resource = {'id': 'resource_id'}
    cr.stdout = json.dumps(resource)

    data = {
        "instance_name": 'instance_name',
        "from_source": 'image',
        "source_name": 'image_name',
        "flavor": 'flavor',
        "network_name": 'network',
    }

    result = pytest_rpc.helpers.create_instance(data, myhost)
    assert result == resource['id']


def test_failure(mocker):
    """Verify create_instance returns None when the server instance has failed
    to be successfully created.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='id_value')

    failed = 'Invalid json'
    cr1.rc = 2
    cr1.stdout = json.dumps(failed)

    data = {
        "instance_name": 'instance_name',
        "from_source": 'image',
        "source_name": 'image_name',
        "flavor": 'flavor',
        "network_name": 'network',
    }

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_instance(data, myhost)
