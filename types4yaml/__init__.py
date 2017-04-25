#!/usr/bin/env python
"""
Types4YAML
==========

Types4YAML is a simple type schema system for JSON/YAML documents.

JSON/YAML objects are hugely convenient for passing around data
across environments/languages/programs. Their ease of construction and
flexibility are a one of their great benefits, but when passing them
across APIs it is convenient to check that they conform to the expected
structure.

To this end, we present the Types4YAML library, which provides classes
for reading type schemas (which are themselves written in JSON/YAML)
and validating JSON/YAML documents against them.

Type Schemas
------------

A type schema is a JSON/YAML document which describes a vocabulary
of conformant objects.  Type schemas contain two kinds of element:
atomic types and constructed types. Atomic types describe indivisible
data objects; constructed types describe objects that are composed of
objects of one or more component types.

The supported atomic types are:

any
    Any data object. Any JSON/YAML data which is well formed satisfies
    the ``any`` type.

string
    Any string object.

date
    A string of the form ``YYYY/MM/DD``.

time
    A string of the form ``HH:mm:ss[.s+]``. Note that fractional seconds
    may be present, but if none are present, a trailing decimal point
    (``.``) should not be present.

datetime
    A string of the form ``YYYY/MM/DD HH:mm:ss[.s+]``. Note that
    fractional seconds may be present, but if none are present, a trailing
    decimal point (``.``) should not be present.

number
    A number data object. This includes integers and floating point
    numbers.  In some libraries, floating point numbers are sometimes
    serialized as strings, so a string which can be converted to a number
    also types correctly.

Constructed types are represented as dictionary object with a single key,
which names the kind of composite object being constructed, and whose
value describes the constituent types, the details of which depend on
the kind of composite object as described below:

oneof: enum
    Describes an enumeration of string values. The value is a list of strings
    that constitute valid values. E.g. ``{'oneof':['heads', 'tails']}``

regex: regex
    Describes a constrained string value. The value is a string comprising
    a regular expression (Python ``re`` flavour), which a data string
    must match to be valid. E.g. ``{'string':'^[A-Z][A-Z]:[0-9][0-9]$'}``.

list: type
    Describes a list value of arbitrary length. The value is a type to
    whichThe elements of the list must all conform to for the list to
    be valid. E.g. ``{'list':'string'}``.  Note that in Python, the list
    type also describes native tuples as well as lists.

tuple: types
    Describes a list of fixed length in which the elements may take on
    different types. The value is a list of types which describes the
    types of the constituent fields. Note that in Python, the tuple type
    also describes native tuples as well as lists.

dict: defn
    Describes a dictionary/map object. The value is a dictionary: the keys
    denote the valid keys in the map, and the values, are the type of the
    data object corresponding to the key. Optional keys are denoted with a
    ``?`` suffix. The special key ``*`` indicates that data objects may
    contain additional keys, whose values conform to the corresponding type.
    E.g. ``{'dict':{'foo':'string', 'bar?':'number', '*':'any'}}``.

union: alts
    Describes an undiscriminated union of types. The value is a list of
    types.  A data object that satisfies any one of the types satisfies
    the union type.  Note: the code for testing whether a data object
    satisfies the union should be assumed to test the data object against
    the given types in order, by default, which could have implications
    for performance.  E.g. ``{'union':['string', {'list':'number'}]}``.

d_u: defn
    Describes a discriminated union type. Discriminated union types are
    equivalent to dictionaries in which all keys are optional, exactly
    one of which must be present in a valid data object. The value is
    a dictionary object, the keys of which are the discriminators (or tags),
    and the corresponding values are the element types associated with
    that discriminator. E.g. ``{'d_u':{'qux':'number', 'wombat':'string'}}``.

with: defns
    Bind names to one or more types, and yield a type. The value is
    a list of length 2 (a tuple). The first element is a dictionary,
    the keys of which are the defined types. The second element is the
    resulting type.  Redefinition of names in nested ``with`` types is
    not currently supported.  E.g. ``{'with': [{'foo':'number'}, {'named':'foo'}]}``

named: name
    Use a named type. The type must be in scope.

The following YAML document specifies the type schema for valid type schemas:

---
with:
-   dictionary: {dict: {'*': {named: type}}}
    types: {list: {named: type}}
    type:
        union:
        - oneof: [any, string, date, time, datetime, number]
        - dict:
            d_u:
                oneof:  {list: string}
                string: string
                list:   {named: type}
                tuple:  {named: types}
                dict:   {named: dictionary}
                d_u:    {named: dictionary}
                union:  {named: types}
                with:
                    tuple:
                    - {named: dictionary}
                    - {named: type}
                named:  string
-   named: type
...

"""

__docformat__ = 'restructuredtext'

import datetime
import re
import StringIO

import yaml

type_definition_of_types = \
"""
---
with:
-   dictionary: {dict: {'*': {named: type}}}
    types: {list: {named: type}}
    type:
        union:
        - oneof: [any, string, date, time, datetime, number]
        - dict:
            d_u:
                oneof:  {list: string}
                string: string
                list:   {named: type}
                tuple:  {named: types}
                dict:   {named: dictionary}
                union:  {named: types}
                d_u:    {named: dictionary}
                with:
                    tuple:
                    - {named: dictionary}
                    - {named: type}
                named:  string
-   named: type
...
"""

type_of_types = yaml.safe_load(StringIO.StringIO(type_definition_of_types))

class BadType(Exception):
    def __init__(self, arg):
        self.args = arg

class WrongType(Exception):
    def __init__(self, arg):
        self.args = arg

class Type(object):
    def __init__(self, _type, validate = True):
        """
        Create a new type object out of a native python object.
        If validate is True, then the type object is validated
        against the type schema for types.
        """

        if validate:
            tot = Type(type_of_types, False)
            if not tot.valid(_type):
                raise BadType, _type

        self._type = _type
        self.ctxt = []

    def valid(self, x, t = None):
        """
        Check a data object to see if it conforms to the type.
        """
        if t is None:
            t = self._type

        if isinstance(t, basestring):
            m = 'valid_atom_' + t
            return getattr(self, m)(x)

        assert type(t) == type({}) and len(t) == 1

        (k, v) = t.items()[0]
        m = 'valid_cons_' + k
        return getattr(self, m)(x, v)

    def valid_atom_string(self, x):
        if not isinstance(x, basestring):
            return False
        return True

    def valid_atom_date(self, x):
        if not isinstance(x, basestring):
            return False
        m = re.match('(\d\d\d\d)/(\d\d)/(\d\d)$', x)
        if m is None:
            return False
        try:
            yy = int(m.group(1))
            mm = int(m.group(2))
            dd = int(m.group(3))
            d = datetime.date(yy, mm, dd)
            return True
        except:
            return False

    def valid_atom_time(self, x):
        if not isinstance(x, basestring):
            return False
        m = re.match('(\d\d):(\d\d):(\d\d)(\.[0-9]+)?$', x)
        if m is None:
            return False
        hh = int(m.group(1))
        mm = int(m.group(2))
        ss = int(m.group(3))
        if m.group(4) is not None:
            ss = float(m.group(3) + m.group(4))
        if hh < 0 or hh >= 24:
            return False
        if mm < 0 or mm >= 60:
            return False
        if ss < 0 or ss >= 60:
            return False
        return True

    def valid_atom_datetime(self, x):
        if not isinstance(x, basestring):
            return False
        m = re.match('(\d\d\d\d/\d\d/\d\d) (\d\d:\d\d:\d\d(\.[0-9]+)?)$', x)
        if m is None:
            return False
        return self.valid_atom_date(m.group(1)) and self.valid_atom_time(m.group(2))

    def valid_atom_number(self, x):
        if isinstance(x, (int, long, float)):
            return True
        try:
            y = float(x)
            return True
        except:
            return False

    def valid_cons_oneof(self, x, t):
        if not isinstance(x, basestring):
            return False
        return x in t

    def valid_cons_regex(self, x, t):
        if not isinstance(x, basestring):
            return False
        try:
            if re.match(t, x):
                return True
            return False
        except:
            return False

    def valid_cons_list(self, x, t):
        if type(x) != type([]) and type(x) != type((1,2)):
            return False
        for i in xrange(len(x)):
            if not self.valid(x[i], t):
                return False
        return True

    def valid_cons_tuple(self, x, t):
        if type(x) != type([]) and type(x) != type((1,2)):
            return False
        if len(x) != len(t):
            return False
        for i in xrange(len(x)):
            if not self.valid(x[i], t[i]):
                return False
        return True

    def valid_cons_dict(self, x, t):
        if type(x) != type({}):
            return False
        mand = {}
        opts = {}
        extra = None
        for (k,u) in t.items():
            if k == '*':
                extra = u
            elif k.endswith('?'):
                opts[k[:-1]] = u
            else:
                mand[k] = u
        xks = set([])
        for (k,y) in x.items():
            if k in mand:
                if not self.valid(y, mand[k]):
                    return False
                continue
            if k in opts:
                if not self.valid(y, opts[k]):
                    return False
                continue
            if extra is not None:
                if not self.valid(y, extra):
                    return False
                continue
            return False
        return True

    def valid_cons_d_u(self, x, t):
        if type(x) != type({}):
            return False
        if len(x) != 1:
            return False
        (k, y) = x.items()[0]
        if k not in t:
            return False
        return self.valid(y, t[k])

    def valid_cons_union(self, x, t):
        for u in t:
            if self.valid(x, u):
                return True
        return False

    def valid_cons_with(self, x, t):
        assert len(t) == 2
        defs = t[0]
        u = t[1]
        self.ctxt.append(defs)
        r = self.valid(x, u)
        self.ctxt.pop()
        return r

    def valid_cons_named(self, x, t):
        for defs in self.ctxt:
            if t in defs:
                return self.valid(x, defs[t])
        raise BadType, t

def make_type(stream):
    """
    Construct a type schema object from a string or file object.
    """
    if isinstance(stream, basestring):
        stream = StringIO.StringIO(stream)
    t = yaml.load(stream)
    return Type(t)
