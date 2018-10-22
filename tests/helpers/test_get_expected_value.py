# -*- coding: utf-8 -*-

"""Test cases for the 'get_expected_value' helper function."""

# ==============================================================================
# Imports
# ==============================================================================
import pytest
from pytest_rpc.helpers import get_expected_value


# ==============================================================================
# Fixtures
# ==============================================================================
@pytest.fixture(scope='module')
def server_info_output():
    """Sample output from running 'openstack server show <SERVER> -f json'."""

    return """
{
  "OS-EXT-STS:task_state": null,
  "addresses": "PRIVATE_NET=192.168.0.18",
  "image": "Cirros-0.3.5 (a4db6a58-2824-4ebc-bcc2-75644443854f)",
  "OS-EXT-STS:vm_state": "active",
  "OS-EXT-SRV-ATTR:instance_name": "instance-0000002e",
  "OS-SRV-USG:launched_at": "2018-10-16T16:24:07.000000",
  "flavor": "m1.tiny (7627a6a5-0d38-4187-afc1-b9dd40d64e80)",
  "id": "ec6c2b98-0751-447f-9562-d8b2bae83a62",
  "security_groups": "name='default'",
  "volumes_attached": "",
  "user_id": "2710bed9364141e8b961a7657d0dde42",
  "OS-DCF:diskConfig": "MANUAL",
  "accessIPv4": "",
  "accessIPv6": "",
  "progress": 0,
  "OS-EXT-STS:power_state": "Running",
  "OS-EXT-AZ:availability_zone": "nova",
  "config_drive": "",
  "status": "ACTIVE",
  "updated": "2018-10-16T16:26:33Z",
  "hostId": "3ea1a7b7666b188cdcb11799daa280318f6580f838d963802871a406",
  "OS-EXT-SRV-ATTR:host": "compute2",
  "OS-SRV-USG:terminated_at": null,
  "key_name": null,
  "properties": "",
  "project_id": "5fed48fa32ca4fd99e6f7543f44cd1f5",
  "OS-EXT-SRV-ATTR:hypervisor_hostname": "compute2.openstack.local",
  "name": "test_instance_01_3A06F",
  "created": "2018-10-16T16:23:54Z"
}
"""


# ==============================================================================
# Tests
# ==============================================================================
def test_get_expected_value_case_insensitive(mocker, server_info_output):
    """Verify get_expected_value returns True when matching against key/values
    that have different cases for the same value with insensitive mode.
    """

    # Mock
    mock_host = mocker.MagicMock()
    mock_host.run.return_value = mocker.MagicMock(stdout=server_info_output)

    # Expectations
    value_exp = 'active'

    # Test
    assert get_expected_value(resource_type='foo',
                              resource_name='bar',
                              key='status',
                              expected_value=value_exp,
                              run_on_host=mock_host,
                              retries=1,
                              case_insensitive=True)

    assert get_expected_value(resource_type='foo',
                              resource_name='bar',
                              key='OS-EXT-STS:vm_state',
                              expected_value=value_exp,
                              run_on_host=mock_host,
                              retries=1,
                              case_insensitive=True)


def test_get_expected_value_case_sensitive(mocker, server_info_output):
    """Verify get_expected_value returns False when matching against key/values
    that have different cases for the same value with sensitive mode.
    """

    # Mock
    mock_host = mocker.MagicMock()
    mock_host.run.return_value = mocker.MagicMock(stdout=server_info_output)

    # Expectations
    value_exp = 'Active'

    # Test
    assert not get_expected_value(resource_type='foo',
                                  resource_name='bar',
                                  key='status',
                                  expected_value=value_exp,
                                  run_on_host=mock_host,
                                  retries=1,
                                  case_insensitive=False)

    assert not get_expected_value(resource_type='foo',
                                  resource_name='bar',
                                  key='OS-EXT-STS:vm_state',
                                  expected_value=value_exp,
                                  run_on_host=mock_host,
                                  retries=1,
                                  case_insensitive=False)


def test_get_expected_value_with_empty_json_output(mocker):
    """Verify get_expected_value returns False when empty JSON is obtained
    via OpenStack query."""

    # Mock
    mock_host = mocker.MagicMock()
    mock_host.run.return_value = mocker.MagicMock(stdout='')

    # Test
    assert not get_expected_value(resource_type='foo',
                                  resource_name='bar',
                                  key='key',
                                  expected_value='baz',
                                  run_on_host=mock_host,
                                  retries=1)


def test_get_expected_value_with_invalid_json_output(mocker):
    """Verify get_expected_value returns False when invalid JSON is obtained
    via OpenStack query."""

    # Mock
    mock_host = mocker.MagicMock()
    mock_host.run.return_value = mocker.MagicMock(stdout='Not JSON!')

    # Test
    assert not get_expected_value(resource_type='foo',
                                  resource_name='bar',
                                  key='key',
                                  expected_value='baz',
                                  run_on_host=mock_host,
                                  retries=1)
