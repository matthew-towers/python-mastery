# Notes from Beazley - Python Mastery chapter 4

Chapter 4 is "Inside Python Objects."

"[T]he entire object system is mostly just an extra layer that's put on top of
dictionaries"

Each instance gets its own private dictionary `__dict__` holding instance data.
Each class has a `__dict__` with its members.

An instance has a `__class__` attribute referring back to its class.

When you read an attribute with `x.name` it may exist either in the local
instance dict or in the class dict, so both may be checked.

Base (ancestor) classes of a class `A` are stored in `A.__bases__`

MRO = Method Resolution Order. To find attributes, Python walks the MRO until
the first match. Found at `A.__mro__`. The MRO has children before parents,
parents in order, but exact rules are complex.  Calls to `super()` return the
next thing in the MRO - that's not necessarily the immediate parent, so don't
think that super = the immediate parent class.  It can go sideways. Example:

```python
class Base:
    def spam(self):
        print("base spam")

class X(Base):
    def spam(self):
        print("X spam")
        super().spam()

class Y(Base):
    def spam(self):
        print("Y spam")
        super().spam()

class M(X, Y):
    pass
```

If we create an `M` and call its spam method, we get X spam, Y spam, base spam.
The MRO for `M` is `M < X < Y < Base < object` while the MRO for `X` is `X <
Base < object`.  So the method order is determined by the initial caller.

This can cause weird problems if you have varying method signatures.

## Descriptors

Access to class attributes involves the "descriptor protocol." This "holds the
whole object system together."

When an attribute is accessed on a class, it is checked to see if it "looks
like" a descriptor: an object with one or more of `__get__(obj, cls)`,
`__set__(obj, val)`, `__delete__(obj)`. If so, the access actually triggers one
of these methods.

Example: create a class `Descriptor` with init, get, set, delete special methods
like above printing debug message. Create a new class with class attributes
`a`, `b` which are `Descriptors`.  Create an instance `f` of your new class and
access `f.a`. The result is that the `a.__get__` method is called.

Descriptors override the instance `__dict__`: if `a` is a descriptor then `f.a =
23` will result in a call to `a`'s set method. It won't overwrite `f.a` with 23.

Instance methods, static methods (via decorators), class methods, properties,
`__slots__` all use descriptors in the implementation. Functions are descriptors
where `__get__()` creates the bound method object. Properties are descriptors.

We can use descriptors to get fine control over data stored in class attributes.
For example:

```python
class Stock:
    shares = Integer('shares')
    ...

class Integer:
    ...
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError
        instance.__dict__[self.name] = value
```

Descriptors can define `__set_name__(self, cls, name)` which receives the name
used as its final arg: `x = Descriptor()` inside class `Spam` invokes
`x.__set_name__(Spam, 'x')`. The point is to avoid redundancies like `shares =
Integer('shares')` above.

## Attribute access

Use `__getattribute__(self, nameOfAttribute)` to intercept attribute access. The default
behaviour is to look for descriptor, check the instance dict, check base
classes. If it still can't find it, invokes `__getattr__(self,
nameOfAttribute)`. This is a failsafe method whose default behaviour is to raise
an `AttributeError`. You could use this to proxy accesses.  Or, you could use it
to restrict which attributes are allowed - the alternative is to use
`__slots__`, but that can't be used with multiple inheritance.
