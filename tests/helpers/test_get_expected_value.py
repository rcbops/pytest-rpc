# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'get_expected_value' helper function."""


def test_get_expected_value_invalid_json(mocker):
    """Verify get_expected_value returns False when invalid JSON is obtained
    via OpenStack query."""
    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout
    assert not pytest_rpc.helpers.get_expected_value('server', 'bar', 'key',
                                                     'expected_value', myhost,
                                                     1)
