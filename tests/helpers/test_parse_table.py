# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'parse_table' helper function."""


def test_empty():
    """Verify parse_table returns a tuple of two empty lists when provided an
    empty string to parse."""

    table_str = ''

    assert pytest_rpc.helpers.parse_table(table_str) == ([], [])


def test_table():
    """Verify parse_table returns lists of headers and rows when provided an
    OpenStack style ascii table."""

    headers = ['ID', 'Name', 'Status', 'State', 'Distributed', 'HA', 'Project']
    row1 = ['16cb7a4b-ffd0-49ef-992c-6d5507a8422c', 'TEST-ROUTER', 'ACTIVE',
            'UP', 'False', 'False', 'ca37d49d3231475ba0d17d9efc043e09']
    row2 = ['9de29825-3af1-447c-b622-4c40b61c9906', 'GATEWAY_NET_ROUTER',
            'ACTIVE', 'UP', 'False', 'False',
            'ca37d49d3231475ba0d17d9efc043e09']
    row3 = ['', '', '', '', '', '', '']
    table_str = """
                +----+----+----+----+----+----+----+
                | {} | {} | {} | {} | {} | {} | {} |
                +----+----+----+----+----+----+----+
                | {} | {} | {} | {} | {} | {} | {} |
                | {} | {} | {} | {} | {} | {} | {} |
                +----+----+----+----+----+----+----+
    """.format(*(headers + row1 + row2))

    assert pytest_rpc.helpers.parse_table(table_str) == (headers, [row1, row2, row3])


def test_garbage():
    """Verify parse_table returns a tuple of two lists when provided a garbage
    string to parse."""

    garbage = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis
    at semper ligula. Mauris gravida elementum enim, in iaculis erat egestas
    vitae. Vivamus sit amet felis a lorem sodales dictum. Donec vitae ante eu
    massa scelerisque malesuada eget non odio. Nulla nec condimentum felis.
    Sed scelerisque commodo neque dignissim rutrum. Nullam ultrices eleifend
    ipsum. Aliquam erat volutpat."""

    result = pytest_rpc.helpers.parse_table(garbage)

    assert type(result) is tuple
    assert len(result) is 2
    assert type(result[0]) is list
    assert type(result[1]) is list
