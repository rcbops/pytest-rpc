# -*- coding: utf-8 -*-
import pytest_rpc.helpers
import json

"""Test cases for the 'get_id_by_name' helper function."""


def test_successful_query(mocker):
    """Verify get_id_by_name returns ID value when OpenStack query is
    successful."""

    test_id = 'test-id'
    out = json.dumps({'id': test_id})
    myout = mocker.MagicMock(stdout=out)
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout

    result = pytest_rpc.helpers.get_id_by_name('server', 'myserver', myhost)
    assert result == test_id


def test_invalid_json(mocker):
    """Verify get_id_by_name returns None when OpenStack query returns invalid
    JSON."""

    myout = mocker.MagicMock(stdout='')
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout

    result = pytest_rpc.helpers.get_id_by_name('server', 'myserver', myhost)
    assert result is None


def test_no_id(mocker):
    """Verify get_id_by_name returns None when OpenStack query returns JSON
    without an id value."""

    out = json.dumps({'foo': 'bar'})
    myout = mocker.MagicMock(stdout=out)
    myhost = mocker.MagicMock()
    myhost.run.return_value = myout

    result = pytest_rpc.helpers.get_id_by_name('server', 'myserver', myhost)
    assert result is None
