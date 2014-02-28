""" This module attempts to make it as easy as possible to make consistent and Pythonic string representations of
    objects. These are the strings that are returned when the built-in function <repr> is called. """

__version__ = '0.0.0'
__author__  = 'Drew A. French'
__email__   = 'rectangletangle@gmail.com'
__url__     = 'github.com/rectangletangle'


import itertools
import unittest

__all__ = ['nonliteral', 'literal', 'truncated_string', 'PrettyStr', 'PrettyFloat', 'PrettyEllipsis']

def nonliteral(object, *args, **kw):
    """ This makes representations that can not be used as literal Python code. """

    almost_a_representation = ' '.join(itertools.chain((object.__class__.__name__,),
                                                       _representation_args_and_kw(*args, **kw)))

    return '<{}>'.format(almost_a_representation)

def literal(object, *args, **kw):
    """ This makes representations that can be used as literal Python code. The return value from this should work when
        used as input to the built-in <eval> function. """

    args_and_kw = ', '.join(_representation_args_and_kw(*args, **kw))

    return '{class_name}({args_and_kw})'.format(class_name=object.__class__.__name__, args_and_kw=args_and_kw)

def _representation_args_and_kw(*args, **kw):
    # <sorted> is used to make the keyword argument order deterministic.
    return itertools.chain((repr(arg) for arg in args),
                           sorted(str(name) + '=' + repr(value) for name, value in kw.items()))

def truncated_string(string, cutoff=77, tail='...'):
    """ This limits the length of a string in a somewhat aesthetically pleasing fashion. """

    if cutoff is None:
        return string
    else:
        return string[:cutoff].rstrip() + tail if len(string) > cutoff else string

# Some built-in types with their representations overridden, in order to make them a little bit more pretty.
PrettyStr = type('PrettyStr', (str,), {'__repr__' : lambda self : str(self)})
PrettyFloat = type('PrettyFloat', (float,), {'__repr__' : lambda self : '%0.4f' % self})
PrettyEllipsis = type('PrettyEllipsis', (), {'__repr__' : lambda self : '...'})

# Tests
class _TestRepresentations(unittest.TestCase):
    def setUp(self):
        self.object = type('Foo', (object,), {})()
        self.args   = (1, 2, 3)
        self.kw     = {'foo' : 35, 'bar' : 40}

class TestLiteral(_TestRepresentations):
    def test_empty(self):
        self.assertEqual(literal(self.object), 'Foo()')

    def test_args(self):
        self.assertEqual(literal(self.object, *self.args), 'Foo(1, 2, 3)')

    def test_kw(self):
        self.assertEqual(literal(self.object, **self.kw), 'Foo(bar=40, foo=35)')

    def test_args_and_kw(self):
        self.assertEqual(literal(self.object, *self.args, **self.kw), 'Foo(1, 2, 3, bar=40, foo=35)')

class TestNonliteral(_TestRepresentations):
    def test_empty(self):
        self.assertEqual(nonliteral(self.object), '<Foo>')

    def test_args(self):
        self.assertEqual(nonliteral(self.object, *self.args), '<Foo 1 2 3>')

    def test_kw(self):
        self.assertEqual(nonliteral(self.object, **self.kw), '<Foo bar=40 foo=35>')

    def test_args_and_kw(self):
        self.assertEqual(nonliteral(self.object, *self.args, **self.kw), '<Foo 1 2 3 bar=40 foo=35>')

class TestTruncatedString(unittest.TestCase):
    def test_truncated(self):
        self.assertEqual(truncated_string('hello world', 6), 'hello...')

    def test_shorter_than_cutoff(self):
        self.assertEqual(truncated_string('hello world', 10000), 'hello world')

    def test_cutoff_is_none(self):
        self.assertEqual(truncated_string('hello world', None), 'hello world')

    def test_tail(self):
        self.assertEqual(truncated_string('hello world', 6, tail='foobar'), 'hellofoobar')

if __name__ == '__main__':
    unittest.main()

