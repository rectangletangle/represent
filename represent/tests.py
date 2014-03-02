
import unittest

from represent import literal, nonliteral, truncated_string

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
