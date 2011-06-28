def baseline(instanciator,inputs):
    """Writes a baseline network from the given inputs to the same number
of outputs, and returns those outputs.
The number of inputs need be a power of 2."""
    n = len(inputs)

    if n == 1:
        return inputs
    elif n> 0 and (n - 1) & n == 0: # test if n is a power of 2
        out0s, out1s = [], []

        for i in xrange(n/2):
            s = instanciator.instanciate('simpleSwitch')

            s.in0, s.in1 = inputs[0], inputs[1]
            del inputs[0:2]

            out0s.append(s.out0)
            out1s.append(s.out1)

        return baseline(instanciator,out0s) + baseline(instanciator,out1s)
    else:
        print """The number of inputs of the baseline network has to be
a (non-negative !) power of two !"""

def qBaseline(instanciator,inputs, x, y, bound = None):
    """Writes a baseline network from the given inputs to the same number
of outputs, and returns those outputs.
The number of inputs need be a power of 2."""
    n = len(inputs)

    if n == 1:
        return inputs
    elif n > 0 and (n - 1) & n == 0: # test if n is a power of 2
        out0s, out1s = [], []

        for i in xrange(n/2):
            s = instanciator.instanciate(\
                    'base.simpleSwitch',\
                    scene = instanciator.scene,\
                    x = x,\
                    y = y + i,\
                    in0 = inputs[0],\
                    in1 = inputs[1],
                    boundRequest = bound,\
                    boundReply = bound)

            del inputs[0:2]

            out0s.append(s.out0)
            out1s.append(s.out1)

        return    qBaseline(instanciator,out0s, x + 1, y, bound)\
                + qBaseline(instanciator,out1s, x + 1, y + n//4, bound)
    else:
        print """The number of inputs of the baseline network has to be
a (non-negative !) power of two !"""
