# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'parse_swift_recon' helper function."""


def test_empty():
    """Verify parse_swift_recon returns an empty lists when provided an
    empty string to parse."""

    recon_str = ''

    assert pytest_rpc.helpers.parse_swift_recon(recon_str) == []


def test_expected_output():
    """Verify parse_table returns a nested list of lists grouped by delimiter
    block when given swift-recon output."""

    swift_recon_out = """
===============================================================================
--> Starting reconnaissance on 3 hosts (object)
===============================================================================
[2018-07-19 15:36:40] Checking ring md5sums
3/3 hosts matched, 0 error[s] while checking hosts.
===============================================================================
[2018-07-19 15:36:40] Checking swift.conf md5sum
3/3 hosts matched, 0 error[s] while checking hosts.
===============================================================================
"""

    result = pytest_rpc.helpers.parse_swift_recon(swift_recon_out)
    assert len(result) == 3  # 3 data blocks in output
    assert len(result[0]) == 1  # 1 line in first data block
    assert len(result[1]) == 2  # 2 lines in second data block
    assert len(result[2]) == 2  # 2 lines in second data block
    assert 'Starting recon' in result[0][0]

    swift_count = next(iter([int(s) for s in result[0][0].split() if
                             s.isdigit()]), None)

    for data in result[1:]:
        assert '0 error' in data[-1], 'Errors found in {}'.format(data[0])
        assert "{}/{} hosts matched".format(swift_count,
                                            swift_count) in data[-1]


def test_garbage():
    """Verify parse_swift_recon returns an empty list when provided a garbage
    string to parse that does not contain a delimeter."""

    garbage = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis
at semper ligula. Mauris gravida elementum enim, in iaculis erat egestas
vitae. Vivamus sit amet felis a lorem sodales dictum. Donec vitae ante eu
massa scelerisque malesuada eget non odio. Nulla nec condimentum felis.
Sed scelerisque commodo neque dignissim rutrum. Nullam ultrices eleifend
ipsum. Aliquam erat volutpat."""

    result = pytest_rpc.helpers.parse_swift_recon(garbage)

    assert type(result) is list
    assert len(result) is 0
