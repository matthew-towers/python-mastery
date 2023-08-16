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

def read_csv_as_dicts(filename, casting_functions):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        rows_as_dicts = []
        for row in rows:
            d = {colname: casting_fn(entry) for colname, casting_fn, entry in
                 zip(headers, casting_functions, row)}
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
        for row in rows:
            records.append(cls.from_row(row))
    return records
