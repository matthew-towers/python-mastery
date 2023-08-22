# teststock.py

import unittest
from stock import *

class TestStock(unittest.TestCase):
    def test_create(self):
        s = Stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_keyword_create(self):
        s = Stock(name='GOOG',shares=100,price=490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_sell(self):
        s = Stock(name='GOOG',shares=100,price=490.1)
        s.sell(30)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 70)
        self.assertEqual(s.price, 490.1)

    def test_from_row(self):
        row = ['GOOG', '100', '490.1']
        s = Stock.from_row(row)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_repr(self):
        s = Stock('GOOG', 100, 490.1)
        self.assertEqual(repr(s), "Stock('GOOG', 100, 490.1)")

    def test_eq(self):
        s = Stock('GOOG', 100, 490.1)
        t = Stock('GOOG', 100, 490.1)
        u = Stock('Goog', 100, 490.1)
        self.assertEqual(s, s)
        self.assertEqual(s, t)
        self.assertFalse(s == u)

    def test_set_shares_to_string(self):
        s = Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
             s.shares = '50'

    def test_set_shares_negative(self):
        s = Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
             s.shares = -50

    def test_set_price_to_string(self):
        s = Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
             s.price = "100.4"

    def test_set_price_negative(self):
        s = Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
             s.price = -100.4

    def test_set_wrong_attribute(self):
        s = Stock('GOOG', 100, 490.1)
        with self.assertRaises(AttributeError):
            s.share = 10
# - Test that setting `shares` to a string raises a `TypeError`
# - Test that setting `shares` to a negative number raises a `ValueError`
# - Test that setting `price` to a string raises a `TypeError`
# - Test that setting `price` to a negative number raises a `ValueError`
# - Test that setting a non-existent attribute `share` raises an `AttributeError`

# - Test that you can create a `Stock` using keyword arguments such as `Stock(name='GOOG',shares=100,price=490.1)`.
# - Test that the `cost` property returns a correct value
# - Test that the `sell()` method correctly updates the shares.
# - Test that the `from_row()` class method creates a new instance from good data.
# - Test that the `__repr__()` method creates a proper representation string.
# - Test the comparison operator method `__eq__()`


if __name__ == '__main__':
    unittest.main()

