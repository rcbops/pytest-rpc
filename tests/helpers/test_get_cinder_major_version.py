# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'get_cinder_major_version' helper function."""


def test_valid_version(mocker):
    """Verify get_cinder_major_version returns the major version when the
    cinder version is set to a valid semantic version.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    cr.rc = 0
    cr.stdout = '3.2.1'
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    assert pytest_rpc.helpers.get_cinder_major_version(myhost) == 3


def test_invalid_version(mocker):
    """Verify get_cinder_major_version returns -1 when the cinder version is
    set to an invalid semantic version.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    cr.rc = 0
    cr.stdout = 'foobar'
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    assert pytest_rpc.helpers.get_cinder_major_version(myhost) == -1


def test_error(mocker):
    """Verify get_cinder_major_version returns -1 when the query for the
    cinder version results in an error.

    relies on mocked objects from testinfra
    """

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)

    cr.rc = 1
    cr.stdout = ''
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    assert pytest_rpc.helpers.get_cinder_major_version(myhost) == -1
