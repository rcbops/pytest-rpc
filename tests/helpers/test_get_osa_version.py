# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'get_osa_version' helper function."""


def test_newton_version():
    """Verify osa versions for newton branch"""
    assert pytest_rpc.helpers.get_osa_version('newton') == ('Newton', '14')


def test_newton_rc_version():
    """Verify osa versions for newton-rc branch"""
    assert pytest_rpc.helpers.get_osa_version('newton-rc') == ('Newton', '14')


def test_pike_version():
    """Verify osa versions for pike branch"""
    assert pytest_rpc.helpers.get_osa_version('pike') == ('Pike', '16')


def test_pike_rc_version():
    """Verify osa versions for pike-rc branch"""
    assert pytest_rpc.helpers.get_osa_version('pike-rc') == ('Pike', '16')


def test_queens_version():
    """Verify osa versions for queens branch"""
    assert pytest_rpc.helpers.get_osa_version('queens') == ('Queens', '17')


def test_queens_rc_version():
    """Verify osa versions for queens-rc branch"""
    assert pytest_rpc.helpers.get_osa_version('queens-rc') == ('Queens', '17')


def test_rocky_version():
    """Verify osa versions for rocky branch"""
    assert pytest_rpc.helpers.get_osa_version('rocky-rc') == ('Rocky', '18')


def test_rocky_rc_version():
    """Verify osa versions for rocky-rc branch"""
    assert pytest_rpc.helpers.get_osa_version('rocky-rc') == ('Rocky', '18')


def test_master_version():
    """Verify osa versions for master branch"""
    assert pytest_rpc.helpers.get_osa_version('master') == ('', '')
