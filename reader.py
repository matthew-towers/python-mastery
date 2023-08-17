# Create a new file `reader.py`.  In that file, define a
# utility function `read_csv_as_dicts()` that reads a file of CSV
# data into a list of dictionaries where the user specifies
# the type conversions for each column.

# Here is how it should work:

# ```python
# >>> import reader
# >>> portfolio = reader.read_csv_as_dicts('Data/portfolio.csv', [str,int,float])
# >>> for s in portfolio:
#          print(s)

# {'name': 'AA', 'shares': 100, 'price': 32.2}
# {'name': 'IBM', 'shares': 50, 'price': 91.1}
# {'name': 'CAT', 'shares': 150, 'price': 83.44}
# {'name': 'MSFT', 'shares': 200, 'price': 51.23}
# {'name': 'GE', 'shares': 95, 'price': 40.37}
# {'name': 'MSFT', 'shares': 50, 'price': 65.1}
# {'name': 'IBM', 'shares': 100, 'price': 70.44}
# >>>
# ```

import csv

from abc import ABC, abstractmethod

class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)

# Ex 3.7: reimplement the `read_csv_as_dicts()` and
# `read_csv_as_instances()` functions to use the classes above

def read_csv_as_dicts(filename, casting_functions):
    rows_as_dicts = [] # say we want it to return an empty list if the open
    # fails
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        parser = DictCSVParser(casting_functions)
        for row in rows:
            d = parser.make_record(headers, row)
            rows_as_dicts.append(d)
    return rows_as_dicts


def read_csv_as_instances(filename, cls):
    '''
    Read a CSV file into a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        parser = InstanceCSVParser(cls)
        for row in rows:
            records.append(parser.make_record(headers, row))
    return records

