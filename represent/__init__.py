""" This module attempts to make it as easy as possible to make consistent and Pythonic string representations of
    objects. These are the strings that are returned when the built-in function <repr> is called. """

__version__ = '0.0.0'
__author__  = 'Drew A. French'
__email__   = 'rectangletangle@gmail.com'
__url__     = 'github.com/rectangletangle'

import itertools

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
