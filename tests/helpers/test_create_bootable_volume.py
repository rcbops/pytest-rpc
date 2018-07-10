# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import pytest

"""Test cases for the 'create_bootable_volume' helper function."""


def test_success(mocker):
    """Verify create_bootable_volume completes without raising an error and
    returns None when the OpenStack command returns an exit code of '0'."""

    myhost = mocker.MagicMock()
    myhost.run.return_value = 0

    def side_effect(expected, command):
        out = myhost.run(command)
        assert out in expected

    myhost.run_expect.side_effect = side_effect

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
    command returns an exit code of '2'."""

    myhost = mocker.MagicMock()
    myhost.run.return_value = 2

    def side_effect(expected, command):
        out = myhost.run(command)
        assert out in expected

    myhost.run_expect.side_effect = side_effect

    data = {
            'volume': {
                'size': '',
                'imageRef': '',
                'name': '',
                'zone': '',
            }
    }
    with pytest.raises(AssertionError):
        pytest_rpc.helpers.create_bootable_volume(data,
                                                  myhost)
