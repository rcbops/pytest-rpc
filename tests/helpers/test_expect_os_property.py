# -*- coding: utf-8 -*-
"""Test cases for the 'expect_os_property' helper function."""
# ==============================================================================
# Imports
# ==============================================================================
import pytest
import openstack.connection
from collections import namedtuple
from pytest_rpc.helpers import expect_os_property


# ==============================================================================
# Fixtures
# ==============================================================================
@pytest.fixture
def fake_os_object():
    """An object that works like a munch.Munch object containing just an ID
    property.

    Returns:
        namedtuple: An object that responds to an attribute lookup.
    """

    FakeOsObject = namedtuple('FakeOsObject', ('id',))

    return FakeOsObject(id='A totally fake UUID!')


# ==============================================================================
# Tests
# ==============================================================================
def test_expect_success(mocker, fake_os_object):
    """Verify that the helper will return True when the expected property and
    value are satisfied on a OpenStack resource.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'server'
    prop_dict = {prop_name_exp: prop_value_exp}

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()
    mock_os_api_conn.get_server.return_value = prop_dict

    # Test
    assert expect_os_property(os_api_conn=mock_os_api_conn,
                              os_service=service_name,
                              os_object=fake_os_object,
                              os_prop_name=prop_name_exp,
                              expected_value=prop_value_exp)


def test_expect_failure(mocker, fake_os_object):
    """Verify that the helper will return False when the expected property and
    value are NOT satisfied on a OpenStack resource.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'server'
    prop_dict = {prop_name_exp: 'wrong'}

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()
    mock_os_api_conn.get_server.return_value = prop_dict

    # Test
    assert not expect_os_property(os_api_conn=mock_os_api_conn,
                                  os_service=service_name,
                                  os_object=fake_os_object,
                                  os_prop_name=prop_name_exp,
                                  expected_value=prop_value_exp,
                                  retries=1)


def test_only_extended_props(mocker, fake_os_object):
    """Verify that the helper respects only searching extended properties.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'server'
    prop_dict = {prop_name_exp: 'wrong',
                 'properties': {prop_name_exp: prop_value_exp}}

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()
    mock_os_api_conn.get_server.return_value = prop_dict

    # Test
    assert expect_os_property(os_api_conn=mock_os_api_conn,
                              os_service=service_name,
                              os_object=fake_os_object,
                              os_prop_name=prop_name_exp,
                              expected_value=prop_value_exp,
                              only_extended_props=True)


def test_case_insensitive_match(mocker, fake_os_object):
    """Verify that the helper matches expected value in regardless of casing.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'server'
    prop_dict = {prop_name_exp: prop_value_exp.capitalize()}

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()
    mock_os_api_conn.get_server.return_value = prop_dict

    # Test
    assert expect_os_property(os_api_conn=mock_os_api_conn,
                              os_service=service_name,
                              os_object=fake_os_object,
                              os_prop_name=prop_name_exp,
                              expected_value=prop_value_exp)


def test_case_sensitive_mismatch(mocker, fake_os_object):
    """Verify that the helper respects matching only with case sensitivity when
    specified by the caller.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'server'
    prop_dict = {prop_name_exp: prop_value_exp.capitalize()}

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()
    mock_os_api_conn.get_server.return_value = prop_dict

    # Test
    assert not expect_os_property(os_api_conn=mock_os_api_conn,
                                  os_service=service_name,
                                  os_object=fake_os_object,
                                  os_prop_name=prop_name_exp,
                                  expected_value=prop_value_exp,
                                  case_insensitive=False,
                                  retries=1)


def test_invalid_service_name(mocker, fake_os_object):
    """Verify that the helper raises the correct exception when the caller
    provides an invalid OpenStack service name.

    Args:
        mocker (MockFixture): A wrapper to the Mock library.
        fake_os_object (namedtuple): An object that responds to an attribute
            lookup. ('id')
    """

    # Expect
    prop_name_exp = 'prop'
    prop_value_exp = 'value'

    # Setup
    service_name = 'oops'

    # Mock
    mocker.patch.object(openstack.connection, 'Connection', autospec=True)
    mock_os_api_conn = openstack.connection.Connection()

    # Test
    with pytest.raises(RuntimeError):
        expect_os_property(os_api_conn=mock_os_api_conn,
                           os_service=service_name,
                           os_object=fake_os_object,
                           os_prop_name=prop_name_exp,
                           expected_value=prop_value_exp)
