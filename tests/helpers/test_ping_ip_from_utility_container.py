# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'ping_ip_from_utility_container' helper function."""


def test_success(mocker):
    """Verify ping_ip_from_utility_container returns True when the ping is
    successful.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    cr.rc = 0
    mocker.patch('testinfra.host.Host.run', return_value=cr)
    ip = '192.168.1.1'

    assert pytest_rpc.helpers.ping_ip_from_utility_container(ip, myhost)


def test_failure(mocker):
    """Verify ping_ip_from_utility_container returns False when the ping is
    unsuccessful.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    cr.rc = 2
    mocker.patch('testinfra.host.Host.run', return_value=cr)
    ip = '192.168.1.1'

    assert not pytest_rpc.helpers.ping_ip_from_utility_container(ip, myhost)
