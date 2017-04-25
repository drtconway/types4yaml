from types4yaml import make_type

def test_make():
    doc = """
    string
    """
    t = make_type(doc)

def test_valid():
    doc = """
    string
    """
    val = "foo"
    t = make_type(doc)
    assert t.valid(val)

def test_invalid():
    doc = """
    string
    """
    val = 1
    t = make_type(doc)
    assert not t.valid(val)
