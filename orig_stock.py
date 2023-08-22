
# Using properties and private attributes, modify the `shares` attribute
# of the `Stock` class so that it can only be assigned a non-negative
# integer value.    In addition, modify the `price` attribute so that it
# can only be assigned a non-negative floating point value.

# The new object should work almost exactly the same as
# the old one except for extra type and value checking.
# class Stock:
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
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Shares must be a non-neg {self._types[1].__name__}")
        elif value < 0:
            raise ValueError(f"Shares must be a non-negative {self._types[1].__name__}")
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Price must be a non-neg {self._types[2].__name__}")
        elif value < 0:
            raise ValueError(f"Price must be non-negative")

        self._price = value


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

# 3.3(b)
from decimal import Decimal
class DStock(Stock):
        _types = (str, int, Decimal)


# 3.1(b): Add a function `read_portfolio()` to your `stock.py` program that
# reads a file of portfolio data into a list of `Stock` objects. Here's how it should work:

def read_portfolio(filename):
    import csv
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        portfolio = []
        for row in rows:
            # portfolio.append(Stock(row[0], int(row[1]), float(row[2])))
            portfolio.append(Stock.from_row(row))
        return portfolio

# ```python
# >>> portfolio = read_portfolio('Data/portfolio.csv')
# >>> for s in portfolio:
#         print(s)

# <__main__.Stock object at 0x3902f0>
# <__main__.Stock object at 0x390270>
# <__main__.Stock object at 0x390330>
# <__main__.Stock object at 0x390370>
# <__main__.Stock object at 0x3903b0>
# <__main__.Stock object at 0x3903f0>
# <__main__.Stock object at 0x390430>
# >>>
# ```

def print_portfolio(pf):
    headers = ["name", "shares", "price"]
    print('%10s %10s %10s' % (headers[0], headers[1], headers[2]))
    print('---------- ' * 3)
    for s in pf: 
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))


# Using __slots__ is a performance optimization, reducing memory usage:

class CheapStock:
    __slots__ = ('name', 'shares', 'price')
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

# Dataclasses allow us to omit some boilerplate

from dataclasses import dataclass

@dataclass
class EasyStock:
    name : str
    shares : int
    price : float

# ...but (like for annotations), types aren't enforced. Another variant is

import typing

class TypedStock(typing.NamedTuple):
    name : str
    shares : int
    price : float

# In older code you may see

from collections import namedtuple

OldStock = namedtuple('Stock', ['name', 'shares', 'price'])

# The main feature of named tuples is immutability
