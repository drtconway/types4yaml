from types4yaml import make_type

def test_make():
    doc = """
    datetime
    """
    t = make_type(doc)

def test_valid():
    doc = """
    datetime
    """
    val = "2017/09/23 12:34:56"
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    datetime
    """
    val = 1
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    datetime
    """
    val = "2017/09/23"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_2():
    doc = """
    datetime
    """
    val = "12:34:56"
    t = make_type(doc)
    assert not t.valid(val)
