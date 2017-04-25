from types4yaml import make_type

def test_make():
    doc = """
    number
    """
    t = make_type(doc)

def test_valid_1():
    doc = """
    number
    """
    val = 20
    t = make_type(doc)
    assert t.valid(val)

def test_valid_2():
    doc = """
    number
    """
    val = 3.14
    t = make_type(doc)
    assert t.valid(val)

def test_valid_3a():
    doc = """
    number
    """
    val = "-12345"
    t = make_type(doc)
    assert t.valid(val)

def test_valid_3b():
    doc = """
    number
    """
    val = "3.14"
    t = make_type(doc)
    assert t.valid(val)

def test_valid_3c():
    doc = """
    number
    """
    val = "3.14e-2"
    t = make_type(doc)
    assert t.valid(val)

def test_invalid_0():
    doc = """
    number
    """
    val = "abc"
    t = make_type(doc)
    assert not t.valid(val)

def test_invalid_1():
    doc = """
    number
    """
    val = ['foo', 'bar']
    t = make_type(doc)
    assert not t.valid(val)
