from logcall import logged, logformat

@logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x,y):
    return x*y

@logged
def add(x,y):
    return x+y

@logged
def sub(x,y):
    return x-y
