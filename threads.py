from itertools import tee,cycle

class thread(object):
    def __init__(self, program, rand, loop = False):
#       p1, p2 = tee(program)
#       self._full_program = p1
#       self._program = p2
        self.waiting  = None
        self.loop     = loop
#       self.prog     = self.generator()
        if loop:
            self.prog = cycle(program)
        else:
            self.prog = program
        self.rand = rand
    
#   def generator(self):
#       if self.loop:
#           while True:
#               try:
#                   yield self._program.next()
#               except StopIteration:
#                   self._program, self._full_program = tee(self._full_program)
#                   yield self._program.next()
#       else:
#           for i in self._program:
#               yield i
