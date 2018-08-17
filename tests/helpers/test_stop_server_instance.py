# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'stop_server_instance' helper function."""


def test_success(mocker):
    """Verify stop_server_instance completes without raising an error and
    returns None when the OpenStack command returns an exit code of '0'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='id_value')

    cr1.rc = 0

    assert not pytest_rpc.helpers.stop_server_instance('myserver', myhost)


def test_failure(mocker):
    """Verify stop_server_instance raises an error when the OpenStack command
    returns an exit code of '2'.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=cr1)
    mocker.patch('pytest_rpc.helpers.get_id_by_name', return_value='id_value')

    cr1.rc = 2

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.stop_server_instance('myserver', myhost)
