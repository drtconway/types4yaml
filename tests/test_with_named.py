from types4yaml import BadType, make_type

import pytest

def test_make_valid_1():
    doc = """
    with:
    - {}
    - string
    """
    t = make_type(doc)

def test_make_valid_2():
    doc = """
    with:
    - foo: string
      bar: number
    - string
    """
    t = make_type(doc)

def test_make_valid_3():
    doc = """
    with:
    - foo: string
      bar: number
    - named: foo
    """
    t = make_type(doc)

def test_make_invalid_1():
    doc = """
    with: string
    """
    with pytest.raises(BadType):
        t = make_type(doc)

def test_make_invalid_2():
    doc = """
    with:
    - foo: string
      bar: number
    - named: baz
    """
    with pytest.raises(BadType):
        t = make_type(doc)
        val = 'foo'
        t.valid(val)

def test_valid_1a():
    doc = """
    with:
    - foo: string
      bar: number
    - named: foo
    """
    t = make_type(doc)
    val = 'qux'
    assert t.valid(val)

def test_valid_1b():
    doc = """
    with:
    - foo: string
      bar: number
    - named: bar
    """
    t = make_type(doc)
    val = 32
    assert t.valid(val)

def test_invalid_1():
    doc = """
    with:
    - foo: string
      bar: number
    - named: foo
    """
    t = make_type(doc)
    val = {'foo': 42}
    assert not t.valid(val)
