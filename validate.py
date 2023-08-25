
# Old version, from 4.2
# class Validator:
#     @classmethod
#     def check(cls, value):
#         return value

# New version for ex 4.3
class Validator:
    def __init__(self, name):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance,	value):
        instance.__dict__[self.name] = self.check(value)


class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

# NB: having classmethods means we don't need to bother creating
# instances.

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

# Now we can make composite validators.

class PositiveInteger(Integer, Positive):
    pass

# The MRO for PositiveInteger is PositiveInteger -> Integer ->
# Typed -> Positive -> Validator -> object (!!)

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass



class Stock:
    __slots__ = ['name', '_shares', '_price']

    _types = (str, int, float) # "private", hence the _

    def __repr__(self):
        return f"Stock('{self.name}', {self.shares}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Stock) and ((self.name, self.shares, self.price) == (other.name, other.shares, other.price))

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = PositiveInteger.check(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        # if (not isinstance(value, self._types[2])) or (value < 0):
        #     raise TypeError(f"Price must be a non-neg {self._types[2].__name__}")
        self._price = PositiveFloat.check(value)


    @property # now we can just do s.cost in place of s.cost()
    def cost(self):
        return self.shares * self.price

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)
    # now even classes that inherit from Stock can correctly use from_row to
    # create instances of themselves using a row


# 3.1(a): Add a new method `sell(nshares)` to Stock that sells a certain number
# of shares by decrementing the share count.  Have it work like this:
    def sell(self, nshares):
        self.shares -= nshares


class VStock:
    name   = String('name')
    shares = PositiveInteger('shares')
    price  = PositiveFloat('price')

    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price

# Ex 6.5

# Modify the `ValidatedFunction` class so that it enforces value checks
# attached via function annotations.  

# Hint: To do this, play around with signature binding. Use the `bind()`
# method of `Signature` objects to bind function arguments to argument
# names.  Then cross reference this information with the
# `__annotations__` attribute to get the different validator classes.

import inspect

class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.annotations = func.__annotations__ # a dict, var name: type

    def __call__(self, *args, **kwargs):
        sig = inspect.signature(self.func)
        # print(sig)
        # print(*args) # uncomment these two to see what's going on with the
        # example of a failure when applying this to a class method from
        # exercise 6.5.
        bin = sig.bind(*args, **kwargs)
        for paramName, value in bin.arguments.items():
            paramType = self.annotations[paramName]
            paramType.check(value)
        result = self.func(*args, **kwargs)
        return result
