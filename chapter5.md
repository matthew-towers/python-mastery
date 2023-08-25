# Things I learned from chapter 5 of Beazley's Python Mastery course

Chapter 5 is on functions.

Standard Python naming convention is that functions have lower case names and
underscores for separation. Internal or private functions should begin with an
underscore.

Standard example for "don't use mutable default arguments":

```python
def f(a=[]):
    a.append(0)
    return a
```

Then successive calls to `f()` produce longer and longer lists of zeroes.

## Futures

```python
from concurrent.futures import Future
def f(x, y, fut):
    time.sleep(20)
    fut.set_result(x+y) # record the output in the Future object

def caller():
    fut = Future()
    threading.Thread(target=f, args=(2, 3, fut)).start()
    result = fut.result() # await the result of the Thread
    print("Got:", result)
```

Future objects are used to wrap results of functions that will run in separate
threads, so we can get them back and work with them.

## Functools

`reduce(f, vals, initial_value)` is left fold.

```python
reduce(lambda x, y: f"({x}*{y})", ["b", "c"], "a")
```

returns `((a*b)*c)`. (Beazley's code for reduce, on p.335 5-30, is something a
bit odd - neither left nor right fold. It would produce `(3*(2*(1*0)))` given a
generic op `*` and the list `[1, 2, 3]` and initial 0).

To note: the true right fold of a generic operation with 0 and `[1, 2, 3]` is
`(1*(2*(3*0)))` so it's wrong to think of 0 as the initial value if that implies
it's getting combined first.  It is combined last!

## Closures

When a function returns a function, the returned value is called a **closure**.
It has to retain the locals of the enclosing function, at least, the ones it
uses.

```python
def add(x, y):
    def do_add():
        print(f'{x} + {y} -> {x+y}')
    return do_add

a = add(3, 4)
```

Now `a.__closure__` contains a tuple of cells, and the `cell_contents` attribute
of the cell contains the values of `x` and `y` passed to the outer function.

**Only** values actually needed syntactically are stored in the closure. For
example

```python
def add(x, y):
    def d():
        print(x+y)
    return d

def add2(x, y):
    z = x+y
    def d():
        print(z)
    return d
```

In the first case the closure will contain two cells, in the second just one.

The values in a closure can be changed, so they can be used as mutable state.

```python
def counter(value):
    def incr():
        nonlocal value
        value += 1
        return value

    def decr():
        nonlocal value
        value -= 1
        return value

    return incr, decr

up, down = counter(0)
```

## Properties and closures

[Here are the property
docs](https://docs.python.org/3/library/functions.html#property).

This one is still confusing me a bit.  I think it's helpful to remember that the
syntax

```python
@decorator
def f(x):
    ...
    return y
```

is roughly (?) equivalent to

```python
def f(x):
    ...
    return y
f = property(f)
```

If you create a property `p` inside a class `C`, you can access it on instances
`c` of `C` with `c.p`. If you wrap a function object in a property, the function
object keeps its closure if it has one - the property doesn't have a closure
because it isn't callable. Example from Exercise 5.4:

```python
def typedproperty(name, expected_type):
    private_name = '_' + name

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, val)
   
    return value
    # value is a property object: type() returns "property"
    # but values returned by typedproperty do not have __closure__ attributes
    # presumably the thing is that it returns properties, not functions
 
class Stock:
    name = typedproperty('name', str) # typedproperty returns a property, so
    # name is a property and we can access it with dot notation as usual
    shares = typedproperty('shares', int)
    price = typedproperty('price', float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
```

## Exceptions

Ariane 5 exploded as a result of an exception handling error.

Reserve Python's built-in exceptions for programming errors.

## Testing

Dynamic nature of Python makes testing more important - there's no compiler
(well, not really) to find bugs.

Assertions should validate program invariants, checking programming errors.

The standard library has `unittest` for testing. Create a file, import the file
with the code you want to test, import unittest.  Define testing classes

```python
class MyTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(myfile.f(2), 4)
```

Can have lots of tests in same class, but methods must start with the word test.
There are assertTrue, assertFalse, assertEqual, assertAlmostEqual (with a places
argument), assertRaises, ...


Finally, add

```python
if __name__ = '__main__':
    unittest.main()
```


