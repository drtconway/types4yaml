from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
        '*': string
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    dict: string
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1():
    doc = """
    dict:
        foo: string
        bar: number
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42}
    assert t.valid(val)

def test_valid_2a():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42}
    assert t.valid(val)

def test_valid_2b():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42, 'baz':'2017/04/25'}
    assert t.valid(val)

def test_valid_2a():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
        '*': number
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42}
    assert t.valid(val)

def test_valid_2b():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
        '*': number
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42, 'quux': 13}
    assert t.valid(val)

def test_valid_2c():
    doc = """
    dict:
        foo: string
        bar: number
        baz?: date
        '*': number
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42, 'quux': 13, 'wombat':23}
    assert t.valid(val)

def test_invalid_1():
    doc = """
    dict:
        foo: string
        bar: number
        baz: date
        '*': number
    """
    t = make_type(doc)
    val = {'foo': 'qux', 'bar': 42, 'quux': 13}
    assert not t.valid(val)

