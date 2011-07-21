from random     import getrandbits, random
from itertools  import ifilter

def bin(n,size = None):
    """
    Returns the binary representation of n
    with enough leading zeros to match  size.
    If size = None, no leading zero is used.

>>> bin(5)
'101'

>>> bin(5,6)
'000101'
"""
    if size == None:
        form_size = ""
    else:
        form_size = str(size)
    return str.format("{0:0>" + form_size + "b}",n)

def randbits(k):
    """Returns a string of random bits of size k"""
    return list(bin(getrandbits(k),k))

def randbool(p, rand = None):
    """Returns True with a probability of p"""
    if rand is None:
        return random() < p
    else:
        return rand.random() < p

def test():
    import doctest
    doctest.testmod()

def iterfile(prog):
    it = (l.strip() for l in ifilter(lambda x: x != "\n", open(prog)))
    for l in it:
        if l == "None":
            yield None
        else:
            yield l

if __name__ == "__main__":
    test()
