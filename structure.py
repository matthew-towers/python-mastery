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

class Structure:
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



class Stock(Structure):
    _fields = ('name','shares','price')

class Date(Structure):
    _fields = ('year', 'month', 'day')
