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

datetime
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

class BadType(Exception):
    def __init__(self, arg):
        self.args = arg

class WrongType(Exception):
    def __init__(self, arg):
        self.args = arg

class Type(object):
    def __init__(self, _type):
        """
        Create a new type object out of a native python object.
        """
        self._type = _type
        self.ctxt = []

    def valid(self, x, t = None):
        if t is None:
            t = self._type

        if isinstance(t, basestring):
            m = 'valid_' + t
            return getattr(m, x, modify)

        assert type(t) == type({}) and len(t) == 1

        (k, v) = t.items()[0]
        m = 'valid_' + k
        return getattr(m, x, v)

    def valid_string(self, x):
        if not isinstance(x, basestring):
            return False
        return True

    def valid_date(self, x):
        if not isinstance(x, basestring):
            return False
        if re.match('\d\d\d\d/\d\d/\d\d$', s):
            return True

    def valid_time(self, x):
        if not isinstance(x, basestring):
            return False
        if re.match('\d\d:\d\d:\d\d$', s):
            return True
        return False

    def valid_datetime(self, x):
        if not isinstance(x, basestring):
            return False
        if re.match('\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d$', s):
            return True
        return False

    def valid_number(self, x):
        if isinstance(x, (int, long, float)):
            return True
        try:
            y = float(x)
            return True
        except ValueError:
            return False

    def valid_oneof(self, x, t):
        if not isinstance(x, basestring):
            return False
        return x in t

    def valid_string(self, x, t):
        if not isinstance(x, basestring):
            return False
        try:
            if re.match(t, x):
                return True
            return False
        except:
            return False

    def valid_list(self, x, t):
        if type(x) != type([]) and type(x) != type((1,2)):
            return False
        for i in xrange(len(x)):
            if not self.valid(x[i], t)
                return False
        return True

    def valid_tuple(self, x, t):
        if type(x) != type([]) and type(x) != type((1,2)):
            return False
        if len(x) != len(t):
            return False
        for i in xrange(len(x)):
            if not self.valid(x[i], t[i])
                return False
        return True

    def valid_dict(self, x, t):
        if type(x) != type({}):
            return False
        # XXX
        return True

    def valid_d_u(self, x, t):
        if type(x) != type({}):
            return False
        # XXX
        return True

    def valid_union(self, x, t):
        for u in t:
            if self.valid(x, u):
                return True
        return False

    def valid_with(self, x, t):
        assert len(t) == 2
        defs = t[0]
        u = t[1]
        self.ctxt.append(defs)
        r = self.valid(x, u)
        self.ctxt.pop()
        return r

    def valid_named(self, x, t):
        for defs in self.ctxt:
            if t in defs:
                return self.valid(x, defs[t])
        return False

def make_type():
    """
    """
    return Type()
