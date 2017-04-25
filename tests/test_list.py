from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    list: string
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    list: wibble
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    list: string
    """
    val = []
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1b():
    doc = """
    list: string
    """
    val = ['foo', 'bar', 'baz']
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1c():
    doc = """
    list: string
    """
    val = ('foo', 'bar', 'baz')
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    list: string
    """
    val = 42
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    list: string
    """
    val = ['foo', 'bar', 'baz', 42]
    t = make_type(doc)
    assert not t.valid(val)

