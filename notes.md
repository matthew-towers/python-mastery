# Notes on Beazley's Python Mastery course

Numbers have some nice methods

```python
x = 123.45
x.as_integer_ratio()
y = 1234
y.numerator
y.denominator
y.is_integer()
y.bit_length()
```

List has `insert(position, item)`

```python
a = [1, 2, 4]
a.insert(2, 3) # a is now [1, 2, 3, 4]
```

`list` on a dict just gives you a list of the keys.

## File reading patterns

```python
with open(filename, 'r') as f:
    data = f.read() # entire file as string, OR
    for line in f:
        ... # line by line
```

```python
with open(filename, 'w') as f:
    f.write('text\n')
```
