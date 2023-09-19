from structure import Structure
from validate import *

class Ticker(Structure):
    name = String("name")
    price =Float("price")
    date = String("date")
    time = String("time")
    change = Float("change")
    open = Float("open")
    high = Float("high")
    low = Float("low")
    volume = Integer("volume")

from cofollow import consumer, follow
from tableformat import create_formatter
import csv

# This one is tricky. See solution for notes about it
@consumer
def to_csv(target):
    def producer():
        while True:
            yield line

    reader = csv.reader(producer())
    while True:
        line = yield
        target.send(next(reader))

@consumer
def create_ticker(target):
    while True:
        row = yield
        target.send(Ticker.from_row(row))

@consumer
def negchange(target):
    while True:
        record = yield
        if record.change < 0:
            target.send(record)

@consumer
def ticker(fmt, fields):
    formatter = create_formatter(fmt)
    formatter.headings(fields)
    while True:
        rec = yield
        row = [getattr(rec, name) for name in fields]
        formatter.row(row) # formatter.row does the printing

if __name__ == "__main__":
    # last = ticker('csv', ["name", "price", "date", "time", "change",
    last = ticker('text', Ticker._fields)

    follow('Data/stocklog.csv', to_csv(create_ticker(negchange(last))) )
