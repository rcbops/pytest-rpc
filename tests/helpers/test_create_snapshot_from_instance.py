# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import testinfra.backend.base
import testinfra.host
import json

"""Test cases for the 'create_snapshot_from_instance' helper function."""


def test_success(mocker):
    """Verify create_snapshot_from_instance returns a resource id when the
    OpenStack command completes successfully.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    server = {'id': 'foo', 'name': 'myserver'}
    cr.rc = 0
    cr.stdout = json.dumps(server)

    result = pytest_rpc.helpers.create_snapshot_from_instance('mysnapshot',
                                                              'myinstance',
                                                              myhost)
    assert result == server['id']


def test_failure(mocker):
    """Verify create_snapshot_from_instance raises an error when the OpenStack
    command returns an exit code of '2'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    cr2 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=[cr1, cr2])

    server = {'id': 'foo', 'name': 'myinstance'}
    cr1.rc = 0
    cr1.stdout = json.dumps(server)
    cr2.rc = 2
    cr2.stdout = 'Invalid json'

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_snapshot_from_instance('mysnapshot',
                                                         'myinstance',
                                                         myhost)
