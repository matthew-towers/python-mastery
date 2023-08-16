import csv

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records

if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    rows = read_rides_as_tuples('Data/ctabus.csv')
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())


def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


import collections

class RideData(collections.abc.Sequence):
    def __init__(self):
        self.routes = []      # Columns
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self): # this and getitem reqd by Sequence
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return { 'route': self.routes[index],
                     'date': self.dates[index],
                     'daytype': self.daytypes[index],
                     'rides': self.numrides[index] }
        else: # it's a slice and has .start, .stop, .step attributes
            # newRideData = RideData()
            # for x in range(index.start, index.stop, index.set):
            #     record = {'route' : self.routes[x],
            #               'date' : self.dates[x],
            #               'daytype' : self.daytypes[x],
            #               'rides': self.numrides[x]}
            #     newRideData.append(record)
            # OR:
            newRideData = RideData()
            newRideData.routes = self.routes[index]
            newRideData.dates = self.dates[index]
            newRideData.daytypes = self.daytypes[index]
            newRideData.numrides = self.numrides[index]
            return newRideData


    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts. Now modified to work with the
    RideData class
    '''
    # records = []
    records = RideData()
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
