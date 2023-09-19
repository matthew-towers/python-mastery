
# Create a new module called `tableformat.py`.  In that program,
# write a function `print_table()` that takes a sequence (list) of objects,
# a list of attribute names, and prints a nicely formatted table. For example:

# ```python
# >>> import stock
# >>> import tableformat
# >>> portfolio = stock.read_portfolio('Data/portfolio.csv')
# >>> tableformat.print_table(portfolio, ['name','shares','price'])
#       name     shares      price
# ---------- ---------- ---------- 
#         AA        100       32.2
#        IBM         50       91.1
#        CAT        150      83.44
#       MSFT        200      51.23
#         GE         95      40.37
#       MSFT         50       65.1
#        IBM        100      70.44

# def print_table(pf, attribs):
#     print(" ".join(['%10s' % attrib for attrib in attribs ]))
#     print("---------- " * len(attribs))
#     for s in pf:
#         print(" ".join(['%10s' % getattr(s, a) for a in attribs]))


# exercise 3.5 
# Ex 3.7: Modify the `TableFormatter` base class so that it is defined as a proper
# abstract base class using the `abc` module.

from abc import ABC, abstractmethod

class TableFormatter(ABC):
    @abstractmethod  # forces subclasses to implement this meth
    def headings(self, headers):
        raise NotImplementedError() # could just pass now since this is an ABC

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()

    def fake(self): # just to show that without the abstractmethod annotation,
                    # subclasses won't have to implement the method
        pass

class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10 + ' ')*len(headers))
    
    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))
    
    def row(self, rowdata):
        print(",".join(map(str, rowdata)))


# <tr> <th>name</th> <th>shares</th> <th>price</th> </tr>
# <tr> <td>AA</td> <td>100</td> <td>32.2</td> </tr>
class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        middle = " ".join(f"<td>{h}</td>" for h in headers)
        print(f"<tr> {middle} </tr>")

    def row(self, rowdata):
        middle = " ".join(f"<td>{d}</td>" for d in rowdata)
        print(f"<tr> {middle} </tr>")

# Ex 3.7: Modify the `print_table()` function  so that it checks if the
# supplied formatter instance inherits from `TableFormatter`.  If
# not, raise a `TypeError`.

def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("formatter must be a TableFormatter or subclass")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)

# Ex 3.8

class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])

# Add a function `create_formatter()` to your `tableformat.py` file that allows
# a user to more easily make a formatter by specifying a format such as
# `'text'`, `'csv'`, or `'html'`.

# Ex 3.8: you wrote a 
# function `create_formatter()` that made it easier to create a custom
# formatter.  Take that function and extend it to understand a few optional
# arguments related to the mixin classes.

# Under the covers the `create_formatter()` function will properly compose
# the classes and return a proper `TableFormatter` instance.

# Example usage: 
# formatter = create_formatter('csv', column_formats=['"%s"','%d','%0.2f'])
# create_formatter('text', upper_headers=True)

def create_formatter(formatname, upper_headers=False, column_formats=('"%s"','%d','%0.2f')):
    # formats = {'text': TextTableFormatter(), 'csv': CSVTableFormatter(),
    #            'html': HTMLTableFormatter()}
    # if formatname in formats:
    #     return formats[formatname]
    # raise Exception("I don't know that format :/")
    #
    # What we should now do: make an appropriate class using a mixin
    if formatname == 'text':
        if upper_headers:
            class PF(UpperHeadersMixin, TextTableFormatter):
                pass
            return PF()
        else:
            return TextTableFormatter()
    if formatname == 'csv':
        class PF(ColumnFormatMixin, CSVTableFormatter):
            formats = column_formats
        return PF()
    raise RuntimeError(f"Format {formatname} unknown")

# the above is particularly horrible. Here's how the solutions do it
# 1) they get the appropriate main formatter_class: TTF, CTF, HTF and raise a
# RuntimeError if none exists
# 2) if column_formats is non-None, they use the appropriate mixin with
# class formatter_class(ColumnFormatMixin, formatter_class) and set formats =
# column_formats (!) inside the class
# 3) if upper_headers is True they do something similar but with empty class
# body
# 4) finally they return formatter_class

# clever way to temporarily change stdout so that prints go to a file:
class redirect_stdout:
    def __init__(self, out_file):
        self.out_file = out_file
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file
    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout
