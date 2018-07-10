# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
from testinfra.backend.base import CommandResult
from testinfra.host import Host
from testinfra.backend.base import BaseBackend

"""Test cases for the 'create_bootable_volume' helper function."""


def test_success(mocker):
    """Verify create_bootable_volume completes without raising an error and
    returns None when the OpenStack command returns an exit code of '0'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=BaseBackend)
    myhost = Host(fake_backend)
    command_result = mocker.Mock(spec=CommandResult)

    command_result.rc = 0
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    data = {
            'volume': {
                'size': '',
                'imageRef': '',
                'name': '',
                'zone': '',
            }
    }
    assert not pytest_rpc.helpers.create_bootable_volume(data, myhost)


def test_failure(mocker):
    """Verify create_bootable_volume raises an error when the OpenStack
    command returns an exit code of '2'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=BaseBackend)
    myhost = Host(fake_backend)
    command_result = mocker.Mock(spec=CommandResult)

    command_result.rc = 2
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    data = {
            'volume': {
                'size': '',
                'imageRef': '',
                'name': '',
                'zone': '',
            }
    }
    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_bootable_volume(data, myhost)
