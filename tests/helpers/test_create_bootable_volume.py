# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'create_bootable_volume' helper function."""


def test_success(mocker):
    """Verify create_bootable_volume returns the volume id when the OpenStack
    command completes successfully

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 0
    command_result.stdout = json.dumps({'id': 'test_id'})
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    data = {
            'volume': {
                'size': '',
                'imageref': '',
                'name': '',
                'zone': '',
            }
    }
    result = pytest_rpc.helpers.create_bootable_volume(data, myhost)
    assert result == 'test_id'


def test_failure(mocker):
    """Verify create_bootable_volume returns None when the OpenStack command
    fails.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    command_result.rc = 2
    command_result.stdout = json.dumps('invalid json')
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    data = {
            'volume': {
                'size': '',
                'imageref': '',
                'name': '',
                'zone': '',
            }
    }

    with pytest.raises(AssertionError):
            pytest_rpc.helpers.create_bootable_volume(data, myhost)
