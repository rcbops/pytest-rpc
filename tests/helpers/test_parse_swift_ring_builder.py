# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'parse_swift_ring_builder' helper function."""


def test_empty():
    """Verify parse_swift_ring_builder returns an empty dictionary when
    provided an empty string to parse."""

    ring_str = ''

    result = pytest_rpc.helpers.parse_swift_ring_builder(ring_str)

    assert type(result) is dict
    assert len(result) is 0


def test_expected_output():
    """Verify parse_swift_ring_builder returns a dictionary with expected key,
    value pairs when given swift-ring-builder output."""

    swift_ring_builder_out = """
Note: using /etc/swift/account.builder instead of /etc/swift/account.ring.gz as builder file

/etc/swift/account.builder, build version 5
256 partitions, 4.000000 replicas, 2 regions, 2 zones, 4 devices, 0.00 balance, 0.00 dispersion
The minimum number of hours before a partition can be reassigned is 1 (0:56:05 remaining)
The overload factor is 0.00% (0.000000)
Ring file /etc/swift/account.ring.gz is up-to-date

Devices:    id  region  zone      ip address  port replication ip  replication port      name weight partitions balance flags meta

             0       1     0     10.240.0.60  6002     10.240.0.60              6002       sdd 100.00        256    0.00
             1       1     0     10.240.0.61  6002     10.240.0.61              6002       sdd 100.00        256    0.00
             2       2     0     10.240.1.60  6002     10.240.1.60              6002       sdd 100.00        256    0.00
             3       2     0     10.240.1.61  6002     10.240.1.61              6002       sdd 100.00        256    0.00
"""  # noqa

    result = \
        pytest_rpc.helpers.parse_swift_ring_builder(swift_ring_builder_out)

    assert type(result) == dict
    assert 'zones' in result.keys()
    assert 'replicas' in result.keys()
    assert 'devices' in result.keys()
    assert 'regions' in result.keys()
    assert 'dispersion' in result.keys()
    assert 'balance' in result.keys()
    assert 'partitions' in result.keys()
    assert type(result['partitions']) == float
    assert result['partitions'] == 256
    assert type(result['dispersion']) == float
    assert result['dispersion'] == 0.00


def test_garbage():
    """Verify parse_swift_ring_builder returns an empty dictionary when provided a
    garbage string to parse."""

    garbage = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis
at semper ligula. Mauris gravida elementum enim, in iaculis erat egestas
vitae. Vivamus sit amet felis a lorem sodales dictum. Donec vitae ante eu
massa scelerisque malesuada eget non odio. Nulla nec condimentum felis.
Sed scelerisque commodo neque dignissim rutrum. Nullam ultrices eleifend
ipsum. Aliquam erat volutpat."""

    result = pytest_rpc.helpers.parse_swift_ring_builder(garbage)

    assert type(result) is dict
    assert len(result) is 0
