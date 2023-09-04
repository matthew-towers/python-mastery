# Beazley - Python Mastery chapter 7 - Metaprogramming

...it's "doing things to code."

## Decorators

Create wrappers around functions. Other code should be able to use the functions
as before, without knowing anything about the wrapper.

Your to-be-a-decorator function must return a function - your replacement for
the thing being wrapped.

Key: 
```python
@deco
def f(...):
    ...
```
is equivalent to

```python
def f(...):
    ...
f = deco(f)
```

Possible uses: logging, timing, debug, dry, optional features...

```python
import time
    def timethis(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            r = func(*args, **kwargs)
            end = time.time()
            print(func.__name__, end - start)
            return r
        return wrapper
```

You can use multiple decorators - they are applied innermost first, so
```python
@a
@b
def f(x):
    ...
```

is equivalent to `f = a(b(f))`

Decorators don't preserve metadata like docstrings. To make this happen:

```python
from functools import wraps

def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

This illustrates decorator arguments - the decoration `@deco(x, y)` is
equivalent to `f = deco(x, y)(f)`. So the decorator must return a function which
is called to make the wrapper.

## Types and classes

A class is an instance of "type"
```python
class Spam:
    pass

type(Spam) # <class 'type'>
```

You can make a class using `type` by specifying name, base class(es), and
methods/attributes: `Spam = type('Spam', (object,), methods)`


## Metaclasses

are classes that create classes, e.g. `type`. There's a `metaclass` kw argument
for class creation that sets the class which will do the creation - its default
is to use the same as the base class.
