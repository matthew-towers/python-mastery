
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

def print_table(pf, attribs):
    print(" ".join(['%10s' % attrib for attrib in attribs ]))
    print("---------- " * len(attribs))
    for s in pf:
        print(" ".join(['%10s' % getattr(s, a) for a in attribs]))
