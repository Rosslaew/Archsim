#! /usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#       pmatching.py
#       
#       Copyright © 2010, Florian Birée <florian@biree.name>
#       
#       This file is a part of Python pattern matching experimentation.
#       
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
#       
###############################################################################
"""Python pattern matching experimentation

This module aim to implement an OCaml-like pattern matching system for Python.

The main object of this module is the match class.

This module is just a proof of concept, and has never been used in production.
"""

__author__ = "Florian Birée"
__version__ = "0.1"
__license__ = "GPL"
__copyright__ = "Copyright © 2010, Florian Birée <florian@biree.name>"
__revision__ = "$Revision: $"
__date__ = "$Date: $"

def kwparam(f, env):
    """Build the param dic of f with values from env
    
    Example:
        >>> env = {'a': 40, 'b': 24, 'c': 2}
        >>> f = lambda a, c: a + c
        >>> kwparam(f, env)
        {'a': 40, 'c': 2}
        >>> f(**kwparam(f, env))
        42
        >>> g = lambda: 42
        >>> kwparam(g, env)
        {}
        >>> g(**kwparam(g, env))
        42
        >>> 
    """
    pdict = {}
    for param in f.__code__.co_varnames[:f.__code__.co_argcount]:
        if param in env:
            pdict[param] = env[param]
    return pdict

class match:
    """A pattern matching 
    You can use this class to define pattern matching:
    
    Compute the sum of 0 to n numbers:
        >>> def sumi(n):
        ...     return match(
        ...         '0 ==', 0,
        ...         lambda: n + (sumi(n - 1)),
        ...     )(n)
        ...
        >>> 
    
    Or, in another way:
        >>> osumi = match(
        ...     '0 ==', 0,
        ...     'n =', lambda rec, n: n + rec(n-1)
        ... )
        >>> 
    
    Note the use of the 'rec' keyword, wich can be used has any parameter of a 
    match body to refer to the match object. This is needed for recursive call,
    because the environment of lambda functions is defined before the match
    object.
    
    Result:
        >>> x = 5
        >>> sumi(x)
        15
        >>> osumi(x)
        15
        >>> 
    
    Iterate over a list (here, do the sum of list elements):
        >>> lsum = match(
        ...     '[e, *t] =', lambda rec, e, t: e + rec(t),
        ...     lambda: 0
        ... )
        >>> lsum([])
        0
        >>> lsum([40, 0, 3, -1])
        42
        >>> 
    
    You can also use more than one pattern to match a sequence instead of one
    object. In this case, you need to specify the number of patterns as the
    first parrameter of the match constructor.
    Exemple : compute the n-first terms of the fibonacci sequence:
        >>> fib = match(3,
        ...     '0 ==', '',      '',      [],
        ...     'n =',  '1 ==',  '1==',   lambda n, rec:
        ...                           [1, 1, 2] + rec(n - 3, 1, 2),
        ...     'n =',  'p_2 =', 'p_1 =', lambda n, p_2, p_1, rec:
        ...                           [p_2 + p_1] + rec(n - 1, p_1, (p_2 + p_1))
        ... )
        >>> fib(7, 1, 1)
        [1, 1, 2, 3, 5, 8, 13]
    
    """
    
    def __init__(self, *cases):
        """Build a new match object"""
        self.cases = []
        if isinstance(cases[0], int):
            nbpatterns = cases[0] + 1
            cases = cases[1:]
        else:
            nbpatterns = 2
        nbitems = len(cases)
        for i in range(nbitems // nbpatterns):
            patterns = cases[i*nbpatterns:(i+1)*nbpatterns-1]
            obj = cases[i*nbpatterns + nbpatterns - 1]
            self.cases.append((patterns, obj))
        if nbitems % nbpatterns:
            self.default = cases[-1]
        else:
            self.default = None
    
    def __call__(self, *args):
        """Call the body wich match the given parameters"""
        initenv = {'__a': args, 'rec': self}
        for (patterns, obj) in self.cases:
            curenv = initenv.copy()
            matched = True
            for i in range(len(patterns)):
                if patterns[i]:
                    pycode = patterns[i] + ('__a[%d] ' % i)
                    try:
                        reseval = eval(pycode, curenv)
                    except:
                        try:
                            exec(pycode, curenv)
                        except:
                            matched = False
                        else:
                            # match!
                            matched = matched and True
                    else:
                        if reseval:
                            # match from eval!
                            matched = matched and True
                        else:
                            matched = False
                else:
                    # empty pattern: always match
                    matched = matched and True
            if matched:
                if hasattr(obj, '__call__'):
                    curenv['__params'] = kwparam(obj, curenv)
                    curenv['__f'] = obj 
                    return eval('__f(**__params)', curenv)
                else:
                    return obj
        if self.default:
            initenv['__f'] = self.default
            return eval('__f()', initenv)
        raise ValueError

if __name__ == '__main__':
    import doctest
    doctest.testmod()
