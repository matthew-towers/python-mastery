# stock.py
from structure import Structure, validate_attributes
from validate import String, PositiveInteger, PositiveFloat

# @validate_attributes
class Stock(Structure):
    name = String('name')
    shares = PositiveInteger('shares')
    price = PositiveFloat('price')

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares : PositiveInteger):
        self.shares -= nshares

# class Stock(Structure):
#     _fields = ('name', 'shares', 'price')
#     name = String('name')
#     shares = PositiveInteger('shares')
#     price = PositiveFloat('price')

#     @property
#     def cost(self):
#         return self.shares * self.price

#     def sell(self, nshares):
#         self.shares -= nshares

# Stock.create_init()
# # stock.py

# from structure import Structure

# class Stock(Structure):
#     _fields = ('name','shares','price')

#     def __init__(self, name, shares, price):
#         self._init()

#     @property
#     def cost(self):
#         return self.shares * self.price

#     def sell(self, nshares):
#         self.shares -= nshares
