from copy import deepcopy as copy
from math import exp
from graphical import segment

class channel(list):
    """A class that extends the lists with more explicit fuctions to match a channel"""

    bound = None
    #def __init__(self):
    #    self.bound = None

    def usage(self):
        """Returns a floting point number representing to what extent
        the component is used.

        The value is between 0. and 1., representing respectively minimum
        and maximum usage."""
        return 1. - exp(-len(self)/5.)

    def read(self):
        """Reads the first value of the channel

        >>> channel([1,2,3]).read()
        1
        """
        if len(self) == 0:
            return None
        else:

            return copy(self[0])

    def write(self,x):
        """Adds an element in the channel
        >>> test = channel()
        >>> test.write(1)
        >>> test.write(2)
        >>> test
        [1, 2]
        """
        self.append(x)

    def pop(self):
        """Deletes the first element of the channel.


        >>> test = channel([1,2])
        >>> test.pop()
        >>> test
        [2]
        """
        del self[0]

    def is_full(self):
        """Tells if the channel is full. Always false for an unbounded channel."""
        return False

class FullChannel(Exception): pass

class boundedChannel(channel):
    def __init__(self,bound=1,*args):
        channel.__init__(self,*args)
        self.bound = bound

    def usage(self):
        """Returns a floting point number representing to what extent
        the component is used.

        The value is between 0. and 1., representing respectively minimum
        and maximum usage."""
        return float(len(self))/float(self.bound)

    def write(self,x):
        if len(self) < self.bound:
            channel.write(self,x)
        else:
            print "Channel full."
            raise FullChannel()

    def is_full(self):
        """Tells is the channel is full. Always false for an unbounded channel."""
        return len(self) >= self.bound

#@segment
class biChannel(object):
    def __init__(self, boundRequest = None, boundReply = None):
        if boundRequest == None:
            self.request = channel()
        else:
            self.request = boundedChannel(boundRequest)
        if boundReply == None:
            self.reply = channel()
        else:
            self.reply = boundedChannel(boundReply)
biChannel = segment(biChannel)

def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()
