
class Finished(Exception):
    pass

cycle = 0L

class simulItem(object): pass

class runner(simulItem):
    def __init__(self, comps):
        from components.base import processor as proc
        self.components = comps

        self.unfinished_procs = filter(lambda x:isinstance(x,proc), self.components)

    def clock(self):
        global cycle
        print "-"*10
        for c in self.components:
            c.clock1()
        for c in self.components:
            try:
                c.clock2()
            except Finished:
                self.components.remove(c)
                self.unfinished_procs.remove(c)
        cycle += 1

    def run(self, nruns = None):
        if nruns == None:
            unfinished_procs = self.unfinished_procs
            while len(unfinished_procs) != 0:
                self.clock()
            print "Finished in %d cycles." % cycle
        else:
            for i in xrange(nruns):
                self.clock()

class instanciator(simulItem):
    def __init__(self):
        self.components = {}
        self.ncomponents = {}

    def instanciate(self, cl, *args, **keys):
        from components import base, bidimensional
        if cl not in self.ncomponents:
            self.ncomponents[cl] = 0

        instance = eval(cl)(*args, **keys)
        instance.name = cl + str(self.ncomponents[cl])
        self.components[cl + str(self.ncomponents[cl])] = instance 
        self.ncomponents[cl] += 1
        return instance

    def make(self,file):
        self.components = {}
        self.ncomponents = {}
        execfile(file)

    def get_components(self):
        return self.components.values()

