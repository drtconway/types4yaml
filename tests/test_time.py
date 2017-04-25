from types4yaml import make_type

def test_make():
    doc = """
    time
    """
    t = make_type(doc)

def test_valid_0():
    doc = """
    time
    """
    val = "12:34:56"
    t = make_type(doc)
    assert t.valid(val)

def test_valid_1():
    doc = """
    time
    """
    val = "12:34:56.789"
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    time
    """
    val = 1
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    time
    """
    val = "12"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_2a():
    doc = """
    time
    """
    val = "32:34:56"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_2b():
    doc = """
    time
    """
    val = "12:74:56"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_2c():
    doc = """
    time
    """
    val = "12:34:96"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_3():
    doc = """
    time
    """
    val = "12:34:56extra"
    t = make_type(doc)
    assert not t.valid(val)

