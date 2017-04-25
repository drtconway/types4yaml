from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    d_u:
        foo: string
        bar: number
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    d_u: string
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    d_u:
        foo: string
        bar: number
    """
    t = make_type(doc)
    val = {'foo': 'qux'}
    assert t.valid(val)

def test_valid_1b():
    doc = """
    d_u:
        foo: string
        bar: number
    """
    t = make_type(doc)
    val = {'bar': 42}
    assert t.valid(val)

def test_invalid_1():
    doc = """
    dict:
        foo: string
        bar: number
    """
    t = make_type(doc)
    val = {'foo': 42}
    assert not t.valid(val)

def test_invalid_2():
    doc = """
    dict:
        foo: string
        bar: number
    """
    t = make_type(doc)
    val = {'qux': 42}
    assert not t.valid(val)

