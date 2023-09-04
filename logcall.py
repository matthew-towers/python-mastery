# logcall.py
from functools import wraps

def logged(func):
    print('Adding logging to', func.__name__)
    @wraps(func) # pass func metadata on to the wrapped function
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

# ex 7.3
# Suppose that you wanted the user to be able to specify a 
# custom message of some sort.

# Define a new decorator `@logformat(fmt)` that accepts
# a format string as an argument and uses `fmt.format(func=func)` to
# format a supplied function into a log message:

def logformat(fmt):
    print('Adding logging to', func.__name__)
    def logged(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=f))
            return f(*args, **kwargs)
        return wrapper
    return logged


