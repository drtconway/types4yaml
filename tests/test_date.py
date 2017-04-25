from types4yaml import make_type

def test_make():
    doc = """
    date
    """
    t = make_type(doc)

def test_valid():
    doc = """
    date
    """
    val = "2017/03/25"
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    date
    """
    val = 1
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    date
    """
    val = "2017"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_2():
    doc = """
    date
    """
    val = "2017/03/99"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_3():
    doc = """
    date
    """
    val = "2017/03/25extra"
    t = make_type(doc)
    assert not t.valid(val)

