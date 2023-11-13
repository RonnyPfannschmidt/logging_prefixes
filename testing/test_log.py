import logging

import pytest

from logging_prefixes import call_sig, call_unlogged, logged


class MyClass:
    @logged()
    def logged_method(self):
        return True

    def unlogged_method(self):
        return True


class MyUnloggedClass(MyClass):
    def logged_method(self):
        return call_unlogged(super().logged_method)

    def unlogged_method(self):
        return call_unlogged(super().unlogged_method)


def test_logged_method_unlogged(caplog):
    assert MyUnloggedClass().logged_method()
    assert not caplog.records


def test_normal_method_unlogged():
    assert MyUnloggedClass().unlogged_method()


def test_normal_method_logged(caplog):
    caplog.set_level(logging.DEBUG, logger="logging_prefixes")
    assert MyClass().logged_method()
    assert caplog.records


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
