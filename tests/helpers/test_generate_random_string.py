# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'generate_random_string' helper function."""


def test_zero_length():
    """Verify generate_random_string returns string of specified length."""

    value = 0

    result = pytest_rpc.helpers.generate_random_string(value)
    assert type(result) == str
    assert '-' not in result
    assert len(result) == value


def test_standard_length():
    """Verify generate_random_string returns string of specified length."""

    value = 10

    result = pytest_rpc.helpers.generate_random_string(value)
    assert type(result) == str
    assert '-' not in result
    assert len(result) == value


def test_too_long():
    """Verify generate_random_string returns string 32 characters in length if
    the maximum threshold is exceeded."""

    value = 33

    result = pytest_rpc.helpers.generate_random_string(value)
    assert type(result) == str
    assert '-' not in result
    assert len(result) < value
