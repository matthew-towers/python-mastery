# What I learned from Python Mastery chapter 6

There's a good reason you might want to use `func(*args, **kwargs)`: to write a
wrapper that can pass arguments through to any function, no matter what its
signature.

## Avoiding boilerplate

The `self.a = a; self.b = b`... pattern in initialisers is annoying. A simple
alternative: have a `_fields` tuple listing the attrib names, make your classes
inherit from a `Structure` class with an `__init__` method that uses `_fields`
and `setattr` to set instance variables.

```python
class Structure:
    def __init__(self, *args):
        for name, arg in zip(self._fields, args):
            setattr(self, name, arg)
```

This doesn't mix well with `help`, e.g. you won't get any useful information
about the signature of the init function for a subclass.  Also it doesn't work
with keyword args.

Another way to approach this is using `locals`.  In a function call you can
inspect `locals()` which is a dictionary of all the arguments passed.  You can
use that to forward the function call to somewhere that deals with it
generically, potentially saving boilerplate. Example:

```python
def _init(locs):
    self = locs.pop('self')
    for n, v in locs.items():
        setattr(self, n, v)

class MyClass:
    def __init__(self, a, b, c):
        _init(locals())
```

Of course, we could just call `_init` explicitly with the arguments given to
`__init__` and use args and kwargs in `_init`.

In fact, there's no need to pass any arguments at all to `_init`. We can get the
locals from the calling function by inspecting the stack frame using
`sys._getframe`:

```python
import sys
def _init():
    locs = sys._getframe(1).f_locals
    self = locs.pop('self')
    for n, v in locs.items():
        setattr(self, n, v)
```

This only works because `__init__` does nothing except call `_init`.  Every
local variable, not just the formal parameters, of the calling function will be
found in `f_locals`.  If we want to fit this into the pattern of inheriting from
a `Structure` class which generates init functions for its subclasses, we could
install `_init` as a `@staticmethod` in `Structure` exactly as it is above.  It
can be static because it doesn't require the `self` argument to be passed.

The last method of building init functions for subclasses using a single method
in a parent class is to generate and execute the code yourself, using a list of
fields from the subclass:

```python
@classmethod
def create_init(cls):
    args = ", ".join(cls._fields)
    code = f'def __init__(self, {args}):\n'
    for field in cls._fields:
        code += f'    self.{field} = {field}\n'
    locs = {}
    exec(code, locs)
    cls.__init__ = locs['__init__']
```

## Builtins

You can `import builtins` and change the built-in functions to do something
else, if you want.  This module is the last one checked during name resolution.

## Functions

The docstring can be any string coming immediately after `def`, not just a
triple-quoted one.  It's available in `f.__doc__`

`__annotations__` is a dict of any type annotations, with the return type in
`f.__annotations__['return']`.

You can add arbitrary attributes to functions, e.g. `f.threadsafe = False`,
which then live in `f.__dict__`.

`f.__code__` has loads of stuff.

## `inspect`

The inspect module lets you get information on functions in a usable form.
`inspect.signature(func)` records formal params and their defaults.
`inspect.signature(func).parameters` has the names of the formals.
`sig.parameters['a'].default` gets the default value, if it exists.

## `eval` and `exec`

`exec` runs with the current local scope, but it can't modify it.

```python
def func():
    x = 10
    exec('x = 15')
    print(x) # 10
```

You can specify the namespaces with `exec(code, [globals [, locals]])`. If you
pass a dict of locals it can be modified:

```python
def f():
    x = 10
    loc = locals()
    exec('x=15', globals(), loc)
    print(x) # 10
    print(loc['x']) # 15
    print(locals()['x']) # 10
    locals()['x'] = 20
    print(x) # 10 !!
```

This seems odd to me, but I think the explanation is in the following sentence
from the [docs](https://docs.python.org/3/library/functions.html#locals):

> Note: The contents of this dictionary should not be modified; changes may not
> affect the values of local and free variables used by the interpreter.

The variable `loc` is a red herring here, since it's just a reference to
`locals()`.  The conclusion is just that you can modify `locals()`, and if you
pass `locals()` to exec then changes will persist after exec runs, but this
doesn't necessarily modify the actual local variables.

We can get information out of the result of doing `exec` by giving it an empty
dictionary `locs`, or one that holds any variables it needs, then having the
code create whatever data we want. Then `locs` will hold any newly created vars.
There's an example in the last part of the boilerplate section above. If you
only want a single object, `eval` will work - this is what
`collections.namedtuple` does under the hood. To see this, do 

```python
from collections import namedtuple
import inspect
print(inspect.getsource(namedtuple))
```

The result is

```python
def namedtuple(typename, field_names, *, rename=False, defaults=None, module=None):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessible by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """

    # Validate the field names.  At the user's option, either generate an error
    # message or automatically replace the field name with a valid name.
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    typename = _sys.intern(str(typename))

    if rename:
        seen = set()
        for index, name in enumerate(field_names):
            if (not name.isidentifier()
                or _iskeyword(name)
                or name.startswith('_')
                or name in seen):
                field_names[index] = f'_{index}'
            seen.add(name)

    for name in [typename] + field_names:
        if type(name) is not str:
            raise TypeError('Type names and field names must be strings')
        if not name.isidentifier():
            raise ValueError('Type names and field names must be valid '
                             f'identifiers: {name!r}')
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a '
                             f'keyword: {name!r}')

    seen = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: '
                             f'{name!r}')
        if name in seen:
            raise ValueError(f'Encountered duplicate field name: {name!r}')
        seen.add(name)

    field_defaults = {}
    if defaults is not None:
        defaults = tuple(defaults)
        if len(defaults) > len(field_names):
            raise TypeError('Got more default values than field names')
        field_defaults = dict(reversed(list(zip(reversed(field_names),
                                                reversed(defaults)))))

    # Variables used in the methods and docstrings
    field_names = tuple(map(_sys.intern, field_names))
    num_fields = len(field_names)
    arg_list = ', '.join(field_names)
    if num_fields == 1:
        arg_list += ','
    repr_fmt = '(' + ', '.join(f'{name}=%r' for name in field_names) + ')'
    tuple_new = tuple.__new__
    _dict, _tuple, _len, _map, _zip = dict, tuple, len, map, zip

    # Create all the named tuple methods to be added to the class namespace

    namespace = {
        '_tuple_new': tuple_new,
        '__builtins__': {},
        '__name__': f'namedtuple_{typename}',
    }
    code = f'lambda _cls, {arg_list}: _tuple_new(_cls, ({arg_list}))'
    __new__ = eval(code, namespace)
    __new__.__name__ = '__new__'
    __new__.__doc__ = f'Create new instance of {typename}({arg_list})'
    if defaults is not None:
        __new__.__defaults__ = defaults

    @classmethod
    def _make(cls, iterable):
        result = tuple_new(cls, iterable)
        if _len(result) != num_fields:
            raise TypeError(f'Expected {num_fields} arguments, got {len(result)}')
        return result

    _make.__func__.__doc__ = (f'Make a new {typename} object from a sequence '
                              'or iterable')

    def _replace(self, /, **kwds):
        result = self._make(_map(kwds.pop, field_names, self))
        if kwds:
            raise ValueError(f'Got unexpected field names: {list(kwds)!r}')
        return result

    _replace.__doc__ = (f'Return a new {typename} object replacing specified '
                        'fields with new values')

    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + repr_fmt % self

    def _asdict(self):
        'Return a new dict which maps field names to their values.'
        return _dict(_zip(self._fields, self))

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return _tuple(self)

    # Modify function metadata to help with introspection and debugging
    for method in (
        __new__,
        _make.__func__,
        _replace,
        __repr__,
        _asdict,
        __getnewargs__,
    ):
        method.__qualname__ = f'{typename}.{method.__name__}'

    # Build-up the class namespace dictionary
    # and use type() to build the result class
    class_namespace = {
        '__doc__': f'{typename}({arg_list})',
        '__slots__': (),
        '_fields': field_names,
        '_field_defaults': field_defaults,
        '__new__': __new__,
        '_make': _make,
        '_replace': _replace,
        '__repr__': __repr__,
        '_asdict': _asdict,
        '__getnewargs__': __getnewargs__,
        '__match_args__': field_names,
    }
    for index, name in enumerate(field_names):
        doc = _sys.intern(f'Alias for field number {index}')
        class_namespace[name] = _tuplegetter(index, doc)

    result = type(typename, (tuple,), class_namespace)

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in environments where
    # sys._getframe is not defined (Jython for example) or sys._getframe is not
    # defined for arguments greater than 0 (IronPython), or where the user has
    # specified a particular module.
    if module is None:
        try:
            module = _sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass
    if module is not None:
        result.__module__ = module

    return result
```

## Callables

Implement the special method `__call__(self, *args, **kwargs)`. You could do
this if you wanted to memoize, for example.


