from threads   import thread
from sys       import maxint
from base      import component
from random    import shuffle, getrandbits as rand, randint, Random
from graphical import circle, half_circle, rectangle

import base
import message
import channels
import simulator

length = 16
def decide(pos, but, dir1, dir2):
    '''Chooses between two directions given the position and the destination'''
    # dir1 = left or up
    # dir2 = right or down
    diff = but - pos
    if (length/2) & diff != 0:
        return dir1
    else:
        return dir2

@rectangle
class switch(component):
    def __init__(self, scene, x, y,
            position,
            upper_chan_up    = None,
            upper_chan_down  = None,
            upper_chan_left  = None,
            upper_chan_right = None,
            lower_chan_up    = None,
            lower_chan_down  = None,
            lower_chan_left  = None,
            lower_chan_right = None,
            proc             = None,
            mem              = None,
            boundRequest     = None,
            boundReply       = None):
        """Creates a 2D switch.

        The scene, x and y arguments are for the graphical display.
        The position argument is the logical position in the grid.
        The proc (resp. mem) argument are either a processor (resp. memory)
        instance or a function that returns an instance of it.
        The other arguments are for the channels.
        """
        component.__init__(self)

        # there are eight channels to initialize. A lot of code to do one thing.
        if upper_chan_up is None:
            upper_chan_up = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(upper_chan_up,channels.biChannel)

        if upper_chan_down is None:
            upper_chan_down = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(upper_chan_down,channels.biChannel)

        if upper_chan_left is None:
            upper_chan_left = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(upper_chan_left,channels.biChannel)

        if upper_chan_right is None:
            upper_chan_right = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(upper_chan_right,channels.biChannel)

        if lower_chan_up is None:
            lower_chan_up = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(lower_chan_up,channels.biChannel)

        if lower_chan_down is None:
            lower_chan_down = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(lower_chan_down,channels.biChannel)

        if lower_chan_left is None:
            lower_chan_left = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(lower_chan_left,channels.biChannel)

        if lower_chan_right is None:
            lower_chan_right = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(lower_chan_right,channels.biChannel)

        upper_chan_up.setP(   70*x+25,70*y+ 5)
        upper_chan_down.setP( 70*x+25,70*y+45)
        upper_chan_left.setP( 70*x+ 5,70*y+25)
        upper_chan_right.setP(70*x+45,70*y+25)
        lower_chan_up.setP(   70*x+25,70*y+ 5)
        lower_chan_down.setP( 70*x+25,70*y+45)
        lower_chan_left.setP( 70*x+ 5,70*y+25)
        lower_chan_right.setP(70*x+45,70*y+25)

        self.upper_chan_up    = upper_chan_up
        self.upper_chan_down  = upper_chan_down
        self.upper_chan_left  = upper_chan_left
        self.upper_chan_right = upper_chan_right
        self.lower_chan_up    = lower_chan_up
        self.lower_chan_down  = lower_chan_down
        self.lower_chan_left  = lower_chan_left
        self.lower_chan_right = lower_chan_right

        # the 2D coordinates of the switch (logical, not graphical)
        self.position   = position

        # the messages waiting to be transmitted 
        self.upper_from_up    = \
        self.upper_from_down  = \
        self.upper_from_left  = \
        self.upper_from_right = \
        self.lower_from_up    = \
        self.lower_from_down  = \
        self.lower_from_left  = \
        self.lower_from_right = \
        self.from_proc = \
        self.from_mem = None

        # we initialize the processor and memory attached to the switch
        if not isinstance(proc,processor):
            proc = proc()
            assert isinstance(proc,processor)
        if proc.channel == None:
            self.to_proc = channels.biChannel(scene, boundRequest, boundReply)
            proc.channel = self.to_proc
        else:
            self.to_proc = proc.channel
        self.to_proc.setP(70*x+ 5,70*y+25)

        if not isinstance(mem,base.memory):
            mem = mem()
            assert isinstance(mem,base.memory)
        if mem.channel == None:
            self.to_mem = channels.biChannel(scene, boundRequest, boundReply)
            mem.channel = self.to_mem
        else:
            self.to_mem = mem.channel
        self.to_mem.setP(70*x+ 5,70*y+25)

        # we have a list of messages to transmit on upper and lower channels
        self.upper = []
        self.lower = []

    def usage(self):
        """Returns a floating point number representing to what extent
        the component is used.

        The value is between 0. and 1., representing respectively minimum
        and maximum usage."""
        return max(\
            self.upper_chan_up.request.usage(),
            self.upper_chan_left.request.usage(),
            self.lower_chan_up.request.usage(),
            self.lower_chan_left.request.usage(),
            self.upper_chan_down.reply.usage(),
            self.upper_chan_right.reply.usage(),
            self.lower_chan_down.reply.usage(),
            self.lower_chan_right.reply.usage()
            )

    def upper_clock1(self):
        self.upper = []

        # we define the "reply" direction as from up-left to down-right
        # first, we get the messages
        from_up    = self.upper_chan_up.request.read()
        from_left  = self.upper_chan_left.request.read()
        from_down  = self.upper_chan_down.reply.read()
        from_right = self.upper_chan_right.reply.read()
        from_proc  = self.to_proc.request.read()

        # then, we store them if possible
        if   from_up == None:
            pass
        elif self.upper_from_up == None:
            self.upper_from_up  = from_up
            self.upper.append("upper_from_up")
            self.upper_chan_up.request.pop()

        if   from_down == None:
            pass
        elif self.upper_from_down == None:
            self.upper_from_down  = from_down
            self.upper.append("upper_from_down")
            self.upper_chan_down.reply.pop()

        if   from_left == None:
            pass
        elif self.upper_from_left == None:
            self.upper_from_left  = from_left
            self.upper.append("upper_from_left")
            self.upper_chan_left.request.pop()

        if   from_right == None:
            pass
        elif self.upper_from_right == None:
            self.upper_from_right  = from_right
            self.upper.append("upper_from_right")
            self.upper_chan_right.reply.pop()

        if   from_proc == None:
            pass
        elif self.from_proc == None:
            self.from_proc  = from_proc
            self.upper.append("from_proc")
            self.to_proc.request.pop()

        shuffle(self.upper)

        # here upper_from_** contain the message from each direction
        # to be transmitted

    def lower_clock1(self):
        self.lower = []

        # we define the "reply" direction as from up-left to down-right
        # first, we get the messages
        from_up    = self.lower_chan_up.request.read()
        from_left  = self.lower_chan_left.request.read()
        from_down  = self.lower_chan_down.reply.read()
        from_right = self.lower_chan_right.reply.read()
        from_mem  = self.to_mem.reply.read()

        # then, we store them if possible
        if   from_up == None:
            pass
        elif self.lower_from_up == None:
            self.lower_from_up  = from_up
            self.lower.append("lower_from_up")
            self.lower_chan_up.request.pop()

        if   from_down == None:
            pass
        elif self.lower_from_down == None:
            self.lower_from_down  = from_down
            self.lower.append("lower_from_down")
            self.lower_chan_down.reply.pop()

        if   from_left == None:
            pass
        elif self.lower_from_left == None:
            self.lower_from_left  = from_left
            self.lower.append("lower_from_left")
            self.lower_chan_left.request.pop()

        if   from_right == None:
            pass
        elif self.lower_from_right == None:
            self.lower_from_right  = from_right
            self.lower.append("lower_from_right")
            self.lower_chan_right.reply.pop()

        if   from_mem == None:
            pass
        elif self.from_mem == None:
            self.from_mem  = from_mem
            self.lower.append("from_mem")
            self.to_mem.reply.pop()

        shuffle(self.lower)

        # here lower_from_** contain the message from each direction
        # to be transmitted

    def clock1(self):
        self.upper_clock1()
        self.lower_clock1()

    def clock2(self):
        for mess in self.upper:
            mess_value = getattr(self, mess)
            if mess_value.dst == self.position:
                # we are over the good memory
                if not self.to_mem.request.is_full():
                    self.to_mem.request.write(mess_value)
                    setattr(self, mess, None)
            elif mess_value.dst[0] == self.position[0]:
                # X coordinate ok, we go through the Y
                direction = decide(
                        self.position[1], mess_value.dst[1],
                        self.upper_chan_up.reply,
                        self.upper_chan_down.request)
                if not direction.is_full():
                    direction.write(mess_value)
                    setattr(self, mess, None)
            else:
                # X coordinate not ok, we go through it
                direction = decide(
                        self.position[0], mess_value.dst[0],
                        self.upper_chan_left.reply,
                        self.upper_chan_right.request)
                if not direction.is_full():
                    direction.write(mess_value)
                    setattr(self, mess, None)

        for mess in self.lower:
            mess_value = getattr(self, mess)
            if mess_value.src == self.position:
                # we are over the good processor
                if not self.to_proc.reply.is_full():
                    self.to_proc.reply.write(mess_value)
                    setattr(self, mess, None)
            elif mess_value.src[0] == self.position[0]:
                # X coordinate ok, we go through the Y
                direction = decide(
                        self.position[1], mess_value.src[1],
                        self.lower_chan_up.reply,
                        self.lower_chan_down.request)
                if not direction.is_full():
                    direction.write(mess_value)
                    setattr(self, mess, None)
            else:
                # X coordinate not ok, we go through it
                direction = decide(
                        self.position[0], mess_value.src[0],
                        self.lower_chan_left.reply,
                        self.lower_chan_right.request)
                if not direction.is_full():
                    direction.write(mess_value)
                    setattr(self, mess, None)

class processor(base.processor):
    def address(self):
        return (rand(self.nbits),rand(self.nbits))

    def __init__(self,scene, x, y, position, p,nbits,channel = None,\
            boundRequest = None, boundReply = None, loadRatio = 1.7):
        base.processor.__init__(self,scene, x, y, p,nbits,channel,\
            boundRequest, boundReply, loadRatio)
        self.position = position

    def clock2(self):
        if self.message is None:
            function = self.produce()
            if function is None:
                return
            self.message = message.message(self.position,self.address(), function , "", cycle=cycle)

        if not self.channel.request.is_full():
            self.channel.request.write(self.message)
            self.message = None

class simpleSPMD(processor):
    seed = randint(0,maxint)

    def __len__(self):
        return len(self.threads)

    def usage(self):
        return self.channel.reply.usage()

    def __init__(self,scene, x, y, ninstr, nthreads,\
            batch_size = float("infinity"), loop = True, *args, **keys):
        processor.__init__(self,scene, x, y, *args,**keys)

        self.rand = Random(self.seed)
        self.program = (processor.produce(self) for i in xrange(ninstr))

        self.threads = [
            thread(
                (processor.produce(self) for i in xrange(ninstr)),
                Random(self.seed),
                loop)
            for i in xrange(nthreads)
            ]
        self.num_instr = 0L
        self.batch_size = batch_size
        self.arrived = []
        self.loop = loop

    def produce(self):
        self.num_instr += 1
        return self.threads[0].prog.next()

    def clock1(self):
        try:
            m = self.channel.reply.read()
            if m is None:
                return
            s = "Message from memory (%d,%d) arrived to (%d,%d) :%d" \
                % (m.dst[0], m.dst[1], self.position[0], self.position[1],
                        simulator.cycle - m.cycle)
            print s
            self.channel.reply.pop()
            self.arrived.append(m.dst)
        except Exception as inst:
            print type(inst), inst, m.function

    def clock2(self):
        thread = self.threads[0]
        self.rand = thread.rand

        if len(self.threads) == 0:
            raise simulator.Finished()
        if  self.threads[0].waiting in self.arrived:
            self.arrived.remove(self.threads[0].waiting)
            self.threads[0].waiting = None
        elif self.threads[0].waiting is not None:
            print "(%d,%d) still awaiting reply from (%d,%d)." %\
                (self.position[0], self.position[1],
                 self.threads[0].waiting[0], self.threads[0].waiting[1])
            self.threads.append(self.threads[0])
            del self.threads[0]
            self.num_instr = 0
            return

        if self.message is None:
            function = self.produce()
            if function is None:
                return

            self.message = message.message(self.position,self.address(), function , "",
                    cycle = simulator.cycle)

        if not self.channel.request.is_full():
            self.channel.request.write(self.message)
            if self.message.function == "load":
                self.threads[0].waiting = self.message.dst
            if self.message.function == "load" or self.num_instr == self.batch_size:
                self.threads.append(self.threads[0])
                del self.threads[0]
                self.num_instr = 0
            self.message = None

        if len(self.threads) ==0:
            raise simulator.Finished()
