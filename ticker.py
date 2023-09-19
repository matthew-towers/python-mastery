from structure import Structure
from validate import *



class Ticker(Structure):
    name = String('name')
    price = Float('price')
    date = String('date')
    time = String('time')
    change = Float('change')
    open = Float('open')
    high = Float('high')
    low = Float('low')
    volume = Integer('volume')

if __name__ == '__main__':
    from follow import follow
    import csv
    from tableformat import create_formatter, print_table

    formatter = create_formatter('text')

    lines = follow('Data/stocklog.csv')
    rows = csv.reader(lines)
    records = (Ticker.from_row(row) for row in rows)
    negative = (rec for rec in records if rec.change < 0)
    print_table(negative, ['name','price','change'], formatter)
