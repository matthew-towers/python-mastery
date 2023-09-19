# Notes on Beazley - Python Mastery chapter 8

## `yield` as an expression

Example:

```python
def match(pattern):
    print('Looking for %s ' % pattern)
    while True:
        line = yield
        if pattern in line:
            print(line)
```

This is a **coroutine**, defining a function to which you *send* values.
You can now do `g = match('python')`, prime it with `g.send(None)`, then
call `g.send("a load of text")`. If the pattern matches, the `match`
function we defined will just echo the text. If you don't start it with
the send None, nothing will happen.  What this does is to advance
execution to the location of the first `yield`.

The send business is annoying, and can be solved by wrapping with
a decorator.

```python
def consumer(f):
    def start(*args, **kwargs):
        cr = f(*args, **kwargs)
        cr.send(None)
        return cr
    return start

@consumer
def match(pattern):
    ...
```

We can use coroutines to chain things together: create a series of
coroutines, use `send()` to pass data along.

```python
import time
def follow(filename, target):
    f = open(filename)
    f.seek(0, 2) # go to end
    while True:
        line = f.readline()
        if line != '':
            target.send(line)
        else:
            time.sleep(0.1)

@consumer
def printer():
    while True:
        line = yield # receive something
        print(line, end=' ')

@consumer
def match(pattern, target):
    while True:
        line = yield
        if pattern in line:
            target.send(line)

follow('access-log', match('python', printer()))
```

## Generator control flow

Generators support forced termination with `.close()` and exception
handling - you can raise one with `.throw()`

```python
def genfunc():
    ...
    try:
        yield item
    except GeneratorExit:
    # .close() was called, clean up
    ...
    return

g.throw(RuntimeError, "you're dead")
```

The last line raises an exception at the `yield` which can be handled
there.

> In general, you can break out of running iteration and resume it later
> if you need to.  You just need to make sure the generator object isn't
> forcefully closed or garbage collected somehow.

## Coroutine control flow

Equally, you can trigger exceptions in coroutines with `c.throw(e)` and
deal with them in a try-except block around the `yield` expression in
the coroutine definition. It doesn't terminate the coroutine when this
happens.

## Managed Generators

> A manager will coordinate the execution of a collection of generators.

## Yield from

> Starting in Python 3.3, a new `yield from` statement can be used to
> delegate generators to another function.  It is a useful way to clean-up
> code that relies on generators.
