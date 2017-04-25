from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    union:
    - string
    - number
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    union: string
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    union:
    - string
    - number
    """
    t = make_type(doc)
    val = 'foo'
    assert t.valid(val)

def test_valid_1b():
    doc = """
    union:
    - string
    - number
    """
    t = make_type(doc)
    val = 42
    assert t.valid(val)

def test_invalid_1():
    doc = """
    union:
    - string
    - number
    """
    t = make_type(doc)
    val = []
    assert not t.valid(val)
