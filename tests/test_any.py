from types4yaml import make_type

def test_make():
    doc = """
    any
    """
    t = make_type(doc)

def test_valid_1():
    doc = """
    any
    """
    val = "foo"
    t = make_type(doc)
    assert t.valid(val)

def test_valid_2():
    doc = """
    any
    """
    val = 42
    t = make_type(doc)
    assert t.valid(val)

def test_valid_3():
    doc = """
    any
    """
    val = ['123', 'abc', 1e-3, {'a':42}]
    t = make_type(doc)
    assert t.valid(val)

