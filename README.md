represent
======
This library provides a simple way to generate Pythonic string representations of objects.

## Usage:
```python
import represent

class Foo:
    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def __repr__(self):
        return represent.literal(self, *self.args, **self.kw)

class Bar(Foo):
    def __repr__(self):
        return represent.nonliteral(self, *self.args, **self.kw)

if __name__ == '__main__':
    print(Foo(1, 2, 3, a='something', b={})) # Prints `Foo(1, 2, 3, a='something', b={})`
    print(Bar(1, 2, 3, a='something', b={})) # Prints `<Bar 1, 2, 3, a='something', b={}>`
```

## Dependencies:
* Python 2.7 - 3.x

## Installation:
```bash
$ python setup.py install
```
