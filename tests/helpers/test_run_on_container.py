# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'run_on_container' helper function."""


def test_expected_constructed_run_command(mocker):
    """Verify run_on_container helper calls `testinfra.host.Host.run` with the
    expected command and that the returned result is a
    `testinfra.CommandResult`.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    command_result = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=command_result)

    cmd = 'ls -al'
    container_type = 'swift'

    expected_run_cmd = ("lxc-attach -n $(lxc-ls -1 | grep {} | head -n 1) "
                        "-- bash -c '{}'".format(container_type, cmd))

    result = pytest_rpc.helpers.run_on_container(cmd, container_type, myhost)
    myhost.run.assert_called_with(expected_run_cmd)
    assert result == command_result
