# /usr/bin/env python3

import pytest


def test_success():
    assert True


def test_fail():
    with pytest.raises(AssertionError):
        assert False
