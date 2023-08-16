import csv

# row = {
#     'route': route,
#     'date': date,
#     'daytype': daytype,
#     'rides': rides,
# }
def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = {'route' : row[0], 'date' : row[1], 'daytype' : row[2],
                      'rides' : int(row[3])}
            records.append(record)
    return records

if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    rows = read_rides_as_tuples('Data/ctabus.csv')
    print('Memory Use (dict): Current %d, Peak %d' % tracemalloc.get_traced_memory())
