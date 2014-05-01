# -*- coding: utf-8 -*-

from watson.common.contextmanagers import suppress


def test_ignored_exception():
    with suppress(Exception):
        raise Exception
    assert True
