# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest
import json
import testinfra.backend.base
import testinfra.host

"""Test cases for the 'delete_instance' helper function."""


def test_successful_deletion(mocker):
    """Verify delete_instance returns None when server instance is
    successfully deleted."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr1 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    cr2 = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', side_effect=[cr1, cr2, cr2])

    server = {'ID': 'foo', 'Name': 'myserver'}
    cr1.rc = cr2.rc = 0
    cr1.stdout = json.dumps(server)
    cr2.stdout = '[]'

    assert not pytest_rpc.helpers.delete_instance('myserver', myhost)


def test_failed_deletion(mocker):
    """Verify delete_instance raises and AssertionError when server instance
    has failed to be successfully deleted."""

    fake_backend = mocker.Mock(spec=testinfra.backend.base.BaseBackend)
    myhost = testinfra.host.Host(fake_backend)
    cr = mocker.Mock(spec=testinfra.backend.base.CommandResult)
    mocker.patch('testinfra.host.Host.run', return_value=cr)

    server = [{'ID': 'foo', 'Name': 'myserver'}]
    cr.rc = 0
    cr.stdout = json.dumps(server)

    with pytest.raises(AssertionError):
        pytest_rpc.helpers.delete_instance('myserver', myhost)
