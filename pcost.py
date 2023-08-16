# The file `Data/portfolio.dat` contains a list of lines with information
# on a portfolio of stocks.  The file looks like this:

# ```
# AA 100 32.20
# IBM 50 91.10
# CAT 150 83.44
# MSFT 200 51.23
# GE 95 40.37
# MSFT 50 65.10
# IBM 100 70.44
# ```

# The first column is the stock name, the second column is the number of
# shares, and the third column is the purchase price of a single share. 

# Write a program called `pcost.py` that opens this file, reads
# all lines, and calculates how much it cost to purchase all of the shares
# in the portfolio. To do this, compute the sum of the second column
# multiplied by the third column.

# Now modified for ex 1.4


# When writing programs that process data, it is common to encounter
# errors related to bad data (malformed, missing fields, etc.).  Modify
# your `pcost.py` program to read the data file `Data/portfolio3.dat`
# and run it (hint: it should crash).

# Modify your function slightly so that it is able to recover from lines
# with bad data.  For example, the conversion functions `int()` and
# `float()` raise a `ValueError` exception if they can't convert the
# input.  Use `try` and `except` to catch and print a warning message
# about lines that can't be parsed.  For example:

# ```
# Couldn't parse: 'C - 53.08\n'
# Reason: invalid literal for int() with base 10: '-'
# Couldn't parse: 'DIS - 34.20\n'
# Reason: invalid literal for int() with base 10: '-'
# ...
# ```

def portfolio_cost(filename):
    with open(filename, 'r') as f:
        sum = 0
        for line in f:
            parts = line.split()
            try:
                amount = int(parts[1])
                price = float(parts[2])
            except ValueError as e:
                print(f"Couldn't parse: {line}Reason: {e}")
                continue
            sum += amount * price
    return sum

if __name__ == '__main__':
    print(portfolio_cost('Data/portfolio3.dat'))
