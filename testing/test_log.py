# -*- coding: utf-8 -*-

import pytest
from logging_prefixes import call_sig, call_unlogged, logged


def test_logged_method_unlogged():
    class MyClass(object):
        @logged()
        def method(self):
            return True

    class AnotherClass(MyClass):
        def method(self):
            return call_unlogged(super(AnotherClass, self).method)

    assert AnotherClass().method()


def test_normal_method_unlogged():
    class MyClass(object):
        def method(self):
            return True

    class AnotherClass(MyClass):
        def method(self):
            return call_unlogged(super(AnotherClass, self).method)

    assert AnotherClass().method()


@pytest.mark.parametrize(
    "args, kwargs, sig",
    [
        ((), {}, "()"),
        ((1,), {}, "(1)"),
        ((), {"a": 1}, "(a=1)"),
        ((1,), {"a": 1}, "(1, a=1)"),
    ],
)
def test_call_sig(args, kwargs, sig):
    assert call_sig(args, kwargs) == sig
