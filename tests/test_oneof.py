from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    oneof: [foo, bar, baz]
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    oneof: []
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    oneof: [foo, bar, baz]
    """
    val = 'foo'
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1b():
    doc = """
    oneof: [foo, bar, baz]
    """
    val = 'baz'
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    oneof: [foo, bar, baz]
    """
    val = 42
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    oneof: [foo, bar, baz]
    """
    val = 'qux'
    t = make_type(doc)
    assert not t.valid(val)

