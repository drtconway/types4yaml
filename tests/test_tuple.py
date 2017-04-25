from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    tuple: [string, number]
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    tuple: string
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    tuple: [string, number, string]
    """
    val = ['foo', 42, 'bar']
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1b():
    doc = """
    tuple: [string, number, string]
    """
    val = ('foo', 42, 'bar')
    t = make_type(doc)
    assert t.valid(val)

def test_valid_2a():
    doc = """
    tuple: [string, number, list: string]
    """
    val = ['foo', 42, ['bar', 'baz']]
    t = make_type(doc)
    assert t.valid(val)

def test_valid_2b():
    doc = """
    tuple: [string, number, list: string]
    """
    val = ('foo', 42, ('bar', 'baz'))
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    tuple: [string, number, string]
    """
    val = 42
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    tuple: [string, number, string]
    """
    val = ('foo', 'bar', 'baz')
    t = make_type(doc)
    assert not t.valid(val)

