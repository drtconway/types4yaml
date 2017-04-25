from types4yaml import BadType, make_type

import pytest

def test_make_valid():
    doc = """
    regex: '[A-F][1-5]'
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    regex: '[A-F][1-5'
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_valid_1a():
    doc = """
    regex: '[A-F][1-5]'
    """
    val = 'A1'
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1b():
    doc = """
    regex: '[A-F][1-5]'
    """
    val = 'F5extra'
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    regex: '[A-F][1-5]'
    """
    val = 42
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    regex: '[A-F][1-5]'
    """
    val = 'qux'
    t = make_type(doc)
    assert not t.valid(val)

