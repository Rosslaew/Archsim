class message(object):
    id = 0L
    def __init__(self,src,dst,function,data, cycle, length=1, to_memory = True):
        """Class defining a message from processor src to memory dst."""
        self.src       = src
        self.dst       = dst
        self.data      = data
        self.cycle     = cycle
        self.length    = length
        self.function  = function
        self.to_memory = to_memory

        self.id = message.id
        message.id += 1
