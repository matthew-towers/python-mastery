# Ex 6.1

# In a file `structure.py`, define a base class
# `Structure` that allows the user to define simple
# data structures as follows:

# ```python
# class Stock(Structure):
#     _fields = ('name','shares','price')

# class Date(Structure):
#     _fields = ('year', 'month', 'day')
# ```
  
# The `Structure` class should define an `__init__()`
# method that takes any number of arguments and which looks for the
# presence of a `_fields` class variable.  Have the method
# populate the instance from the attribute names in `_fields`
# and values passed to `__init__()`.

# Give the `Structure` class a `__setattr__()` method that restricts
# the allowed set of attributes to those listed in the `_fields` variable.
# However, it should still allow any "private" attribute (e.g., name starting
# with `_` to be set). 

import sys
import inspect
from validate import *
# from validate import Validator, validated

def validate_attributes(cls):
    validators = []
    for name, val in vars(cls).items():
        if isinstance(val, Validator):
            validators.append(val)
        elif callable(val) and val.__annotations__:
            setattr(cls, name, validated(val))
    cls._types = tuple([ getattr(v, 'expected_type', lambda x: x)
                   for v in validators ])
    cls._fields = tuple([v.name for v in validators])
    if cls._fields:
        cls.create_init()
    return cls

class Structure:
    _types = ()
    # def __init__(self, *args):
    #     if len(args) != len(self._fields):
    #         raise TypeError(f"Expected {len(self._fields)} arguments")
    #     for field, val in zip(self._fields, args):
    #         self.__setattr__(field, val)

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs.pop('self')
        for name, val in locs.items():
            setattr(self, name, val)

    def __repr__(self):
        classname = self.__class__.__name__
        args = ", ".join(repr(self.__getattribute__(field)) for field in self._fields)
        return f"{classname}({args})"

    def __setattr__(self, attrname, val):
        if (attrname[0] == "_") or (attrname in self._fields):
            super().__setattr__(attrname, val)
        else:
            raise AttributeError('No attribute %s' % attrname)

    @classmethod
    def set_fields(cls):
        # ex 6.3:
        # inspect __init__ to get the arg names
        # then set the _fields variable accordingly
        # This is for an older version of the subclasses with no fields class
        # var
        params = list(inspect.signature(cls.__init__).parameters)
        cls._fields = tuple(params[1:])

    # My solution:
    # @classmethod
    # def create_init(cls):
    #     args = ", ".join(cls._fields)
    #     code = f'def __init__(self, {args}):\n'
    #     for field in cls._fields:
    #         code += f'    self.{field} = {field}\n'
    #     locs = {}
    #     exec(code, locs)
    #     cls.__init__ = locs['__init__']

    # official solution:
    @classmethod
    def create_init(cls):
        args = ','.join(cls._fields)
        code = 'def __init__(self, {0}):\n'.format(args)
        statements = [ '    self.{0} = {0}'.format(name) for name in cls._fields]
        code += '\n'.join(statements)
        locs = { }
        exec(code, locs)
        cls.__init__ = locs['__init__']

    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

class Stock(Structure):
    _fields = ('name','shares','price')
    # def __init__(self, name, shares, price):
    #     self._init()

class Date(Structure):
    _fields = ('year', 'month', 'day')
    # def __init__(self, year, month, day):
    #     self._init()


# ex 7.4
def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators)
    return cls
