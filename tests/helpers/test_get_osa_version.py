# -*- coding: utf-8 -*-
import pytest_rpc.helpers

"""Test cases for the 'get_osa_version' helper function."""


def test_newton_version(monkeypatch):
    """Verify osa versions for newton branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'newton')
    assert pytest_rpc.helpers.get_osa_version() == (r'Newton', r'14')


def test_newton_rc_version(monkeypatch):
    """Verify osa versions for newton-rc branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'newton-rc')
    assert pytest_rpc.helpers.get_osa_version() == (r'Newton', r'14')


def test_pike_version(monkeypatch):
    """Verify osa versions for pike branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'pike')
    assert pytest_rpc.helpers.get_osa_version() == (r'Pike', r'16')


def test_pike_rc_version(monkeypatch):
    """Verify osa versions for pike-rc branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'pike-rc')
    assert pytest_rpc.helpers.get_osa_version() == (r'Pike', r'16')


def test_queens_version(monkeypatch):
    """Verify osa versions for queens branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'queens')
    assert pytest_rpc.helpers.get_osa_version() == (r'Queens', r'17')


def test_queens_rc_version(monkeypatch):
    """Verify osa versions for queens-rc branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'queens-rc')
    assert pytest_rpc.helpers.get_osa_version() == (r'Queens', r'17')


def test_master_version(monkeypatch):
    """Verify osa versions for master branch"""
    monkeypatch.setattr(pytest_rpc.helpers, 'get_git_branch', lambda: 'master')
    assert pytest_rpc.helpers.get_osa_version() == (r'\w+', r'\w+')
