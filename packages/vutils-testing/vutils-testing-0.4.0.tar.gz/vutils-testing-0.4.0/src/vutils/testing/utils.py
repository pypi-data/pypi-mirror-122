#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-14 17:12:48 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Miscellaneous utilities."""

import importlib
from typing import TYPE_CHECKING, Iterable, Optional

from vutils.testing.mock import PatcherFactory

if TYPE_CHECKING:
    from unittest import TestCase

    from vutils.testing import (
        _BasesType,
        _ExcSpecType,
        _FuncType,
        _MembersType,
    )


def make_type(
    name: str,
    bases: "_BasesType" = None,
    members: "_MembersType" = None,
    **kwargs: object,
) -> type:
    """
    Make a new type.

    :param name: The type name
    :param bases: The type's bases
    :param members: The definition of type's members and methods
    :param kwargs: Additional arguments passed to `type`
    :return: the new type

    This function becomes handy when creating types used as test data. For
    instance, instead of ::

        class ErrorA(Exception):
            pass

        class ErrorB(Exception):
            pass

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = ErrorA
                self.error_b = ErrorB

    it is possible to write::

        class MyTestCase(TestCase):

            def setUp(self):
                self.error_a = make_type("ErrorA", Exception)
                self.error_b = make_type("ErrorB", Exception)

    This helps to keep test data in the proper scope and to reduce the size of
    the code base.
    """
    if bases is None:
        bases = ()
    if not isinstance(bases, tuple):
        bases = (bases,)
    if members is None:
        members = {}
    return type(name, bases, members, **kwargs)


class AssertRaises:
    """
    Wrapper that asserts that callable raises.

    Consider there are two functions ``func1`` and ``func2`` that are very
    similar to each other except ``func2`` raises an exception. Since their
    similarity, the test case defines a function ``run_and_verify(func)`` which
    runs them and test their results and side-effects. However, since ``func2``
    raises an exception, ``run_and_verify(func2)`` fails. To deal with such a
    situation, `AssertRaises` can be used::

        class MyTestCase(CommonTestCase):

            def test_funcs(self):
                wfunc2 = AssertRaises(self, func2, FooError)

                # run_and_verify is defined in CommonTestCase
                self.run_and_verify(func1)
                # Does not fail, exception is caught and stored for later use
                self.run_and_verify(wfunc2)
                # Analyze caught exception
                self.assertEqual(wfunc2.get_exception().detail, "foo")
    """

    __slots__ = ("__testcase", "__func", "__raises", "__exception")

    def __init__(
        self, testcase: "TestCase", func: "_FuncType", raises: "_ExcSpecType"
    ) -> None:
        """
        Initialize the wrapper.

        :param testcase: The test case
        :param func: The callable object to be tested
        :param raises: The expected exceptions
        """
        self.__testcase: "TestCase" = testcase
        self.__func: "_FuncType" = func
        if not isinstance(raises, tuple):
            raises = (raises,)
        self.__raises: "_ExcSpecType" = raises
        self.__exception: Optional[Exception] = None

    def get_exception(self) -> Optional[Exception]:
        """
        Get the caught exception.

        :return: the caught exception object

        When called, *self* is cleared (the next call will return `None`).
        """
        exc: Optional[Exception] = self.__exception
        self.__exception = None
        return exc

    def __call__(self, *args: object, **kwargs: object) -> None:
        """
        Invoke the callable object.

        :param args: Positional arguments
        :param kwargs: Key-value arguments

        Invoke the callable object with *args* and *kwargs*, catch and store
        the exception. Fail if the exception is not raised by the callable
        object or if it is not in the list of expected exceptions.
        """
        with self.__testcase.assertRaises(self.__raises) as catcher:
            self.__func(*args, **kwargs)
        self.__exception = catcher.exception


class TypingPatcher(PatcherFactory):
    """Patch type hints."""

    __slots__ = ()

    def setup(self) -> None:
        """Set up the patcher."""
        self.add_spec("typing.TYPE_CHECKING", new=True)

    def extend(self, target: str, symbols: Iterable[str]) -> None:
        """
        Specify patches for *symbols*.

        :param target: The target module
        :param symbols: The list of symbols to be patched in the *target*
        """
        for symbol in symbols:
            self.add_spec(f"{target}.{symbol}", new=symbol, create=True)


def cover_typing(name: str, symbols: Iterable[str]) -> None:
    """
    Cover the ``if typing.TYPE_CHECKING`` branch.

    :param name: The module name
    :param symbols: The list of symbols

    To make the code like ::

        if typing.TYPE_CHECKING:
            from foo import _TypeA, _TypeB

    in ``foo.bar`` module covered by tests, call ::

        cover_typing("foo.bar", ["_TypeA", "_TypeB"])

    in the test code after imports.
    """
    module = importlib.import_module(name)
    patcher = TypingPatcher()
    patcher.extend(name.rsplit(".", 1)[0], symbols)

    with patcher.patch():
        importlib.reload(module)
    importlib.reload(module)
