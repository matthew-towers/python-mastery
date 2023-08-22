import csv


# Ex 5.1: Create two new functions `csv_as_dicts(lines, types)` and
# `csv_as_instances(lines, cls)` that convert any iterable sequence of
# lines.
# should we be using csv.reader on this iterable seq??
# we should somehow assume
def csv_as_instances(lines, cls, headers=None):
    rows = csv.reader(lines)
    if headers is None: # not specified, so they're in the rows
        headers = next(rows)  # throw it away? "cls" must know the line structure
    return [cls.from_row(row) for row in rows]

def csv_as_dicts(lines, types, headers=None):
    rows = csv.reader(lines)
    if headers is None: # they weren't specified, so they're in the rows
        headers = next(rows)
    return [{name: func(val) for name, func, val in zip(headers, types, row)}
            for row in rows]
 
# To maintain backwards compatibility with older code, write functions
# `read_csv_as_dicts()` and `read_csv_as_instances()` that take a
# filename as before.  These functions should call `open()` on the
# supplied filename and use the new `csv_as_dicts()` or
# `csv_as_instances()` functions on the resulting file.

def read_csv_as_dicts(filename, types, headers=None):
    with open(filename) as f:
        return csv_as_dicts(f, types, headers)

def read_csv_as_instances(filename, cls, headers=None):
    with open(filename) as f:
        return csv_as_instances(f, cls, headers)

# exercise 5.3 then 5.5

# Instead of crashing on bad data, modify the code to issue a warning message
# instead. The final result should be a list of the rows that were successfully
# converted.

def convert_csv(lines, converter, headers=None):
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    # return [converter(headers, row) for row in rows]
    # return list(map(lambda x: converter(headers, x), rows))
    output = []
    for row in rows:
        try:
            output.append(converter(headers, row))
        except ValueError as e:
            print(f"bad row: {row}")
            continue
    return output



def csv_as_instances(lines, cls, headers=None):
    return convert_csv(lines, lambda h, r: cls.from_row(r), headers)

def csv_as_dicts(lines, types, headers=None):
    return convert_csv(lines, lambda h, r: dict(zip(h, [t(x) for t, x in
                                                        zip(types, r)])),
                                                headers)
