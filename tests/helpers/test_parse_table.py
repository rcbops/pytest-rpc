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
