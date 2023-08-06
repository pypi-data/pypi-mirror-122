#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/common.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-22 23:46:47 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Shared test code and data."""

SYMBOLS = (
    "_ReturnsType",
    "_SetupFuncType",
    "_BasesType",
    "_MembersType",
    "_ExcSpecType",
    "_FuncType",
    "_make_patch",
)
FOO_CONSTANT = 42


class FooError(Exception):
    """Dummy exception."""

    __slots__ = ("detail",)

    def __init__(self, detail):
        """
        Initialize the exception object.

        :param detail: The error detail
        """
        Exception.__init__(self, detail)
        self.detail = detail


def func_a(mock):
    """
    Modify *mock*.

    :param mock: The mock object
    """
    mock.foo = FOO_CONSTANT


def func_b(mock):
    """
    Modify *mock* and raise `FooError`.

    :param mock: The mock object
    :raises FooError: when called
    """
    func_a(mock)
    raise FooError(FOO_CONSTANT)
