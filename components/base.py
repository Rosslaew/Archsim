from   random    import randint as rand, Random
from   copy      import deepcopy as copy
from   util      import bin,randbool,randbits
from   threads   import thread
from   graphical import circle, half_circle, rectangle
from   sys       import maxint
import channels
import message
import simulator

class component(object):
    """An abstract component."""
    id = 0
    name = ""

    def clock(self):
        """Executes one clock cycle."""
        self.clock1()
        self.clock2()

    def clock1(self):
        """Fetches the messages to propagate. First part of the clock cycle."""
        pass

    def clock2(self):
        """Propagate the messages. Second part of the clock cycle."""
        pass

    def __init__(self):
        self.id = component.id
        component.id += 1

#--------------------------------------------------------------------------------


@rectangle
class simpleSwitch(component):
    """A switch used in a multistage network"""
    def onConflict(self):
        pass

    def usage(self):
        """Returns a floating point number representing to what extent
        the component is used.

        The value is between 0. and 1., representing respectively minimum
        and maximum usage."""
        return max(\
                self.in0.request.usage(),\
                self.in1.request.usage(),\
                self.out0.reply.usage(),\
                self.out1.reply.usage())

    def __init__(self,scene, x, y,\
            in0=None,\
            in1=None,\
            out0=None,\
            out1=None,\
            boundRequest = None,\
            boundReply = None,\
            onConflict = None):
        component.__init__(self)

        if in0 is None:
            self.in0 = in0 = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(in0,channels.biChannel)
            self.in0 = in0

        if in1 is None:
            self.in1 = in1 = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(in1,channels.biChannel)
            self.in1 = in1

        if out0 is None:
            self.out0 = out0 = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(out0,channels.biChannel)
            self.out0 = out0

        if out1 is None:
            self.out1 = out1 = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(out1,channels.biChannel)
            self.out1 = out1

        in0.setP(70*x+5, 70*y+15)
        in1.setP(70*x+5, 70*y+45)
        out0.setP(70*x+45, 70*y+15)
        out1.setP(70*x+45, 70*y+45)

        self.req0 = None
        self.req1 = None
        self.rep0 = None
        self.rep1 = None

        if onConflict is not None:
            self.onConflict = onConflict
        print "Simple switch", self.id

    def clock1(self):
        """Fetches the messages to propagate. First part of the clock cycle."""
        in0request  = self.in0.request
        in0reply    = self.in0.reply
        in1request  = self.in1.request
        in1reply    = self.in1.reply
        out0request = self.out0.request
        out0reply   = self.out0.reply
        out1request = self.out1.request
        out1reply   = self.out1.reply

        # from input to output
        in0 = in0request.read()
        in1 = in1request.read()

        if in0 is None and in1 is None:
            pass
        elif in0 is None: # in1 is not None
            dst1 = in1.dst.pop()
            in1.src.append('1')
            if dst1 == '0' and not out0request.is_full():
                self.req0 = in1
                in1request.pop()
            elif not out1request.is_full():
                self.req1 = in1
                in1request.pop()
        elif in1 is None: # in0 is not None
            dst0 = in0.dst.pop()
            in0.src.append('0')
            if dst0 == '0' and not out0request.is_full():
                self.req0 = in0
                in0request.pop()
            elif not out1request.is_full():
                self.req1 = in0
                in0request.pop()
        else: # in0 is not None and in1 is not None
            dst0 = in0.dst.pop()
            dst1 = in1.dst.pop()
            if dst0 != dst1: # no conflict
                in0.src.append('0')
                in1.src.append('1')
                if dst0 == '0' and dst1 == '1':
                    if not out0request.is_full():
                        self.req0 = in0
                        in0request.pop()
                    if not out1request.is_full():
                        self.req1 = in1
                        in1request.pop()
                else:
                    if not out0request.is_full():
                        self.req0 = in1
                        in1request.pop()
                    if not out1request.is_full():
                        self.req1 = in0
                        in0request.pop()
#            elif in0.dst == in1.dst: # multicast so still no conflict
#                message = in0
#                message.src.append('x')
#                if   dst0 == '0' and not out0request.is_full(): # dst0 == dst1
#                    self.req0 = message
#                    in0request.pop()
#                    in1request.pop()
#                elif dst0 == '1' and not out1request.is_full():
#                    self.req1 = message
#                    in0request.pop()
#                    in1request.pop()
            else: # conflict
                #print "Conflict on request (switch", self.id, ")"
                self.onConflict()

                # A random strategy is used but any other arbiter 
                # would do.
                if rand(0,1) == 0:
                    in0.src.append('0')
                    if   dst0 == '0' and not out0request.is_full():
                        self.req0 = in0
                        in0request.pop()
                    elif dst0 == '1' and not out1request.is_full():
                        self.req1 = in0
                        in0request.pop()
                else:
                    in1.src.append('1')
                    if   dst1 == '0' and not out0request.is_full():
                        self.req0 = in1
                        in1request.pop()
                    elif dst0 == '1' and not out1request.is_full():
                        self.req1 = in1
                        in1request.pop()

        # from output to input
        out0 = out0reply.read()
        out1 = out1reply.read()

        if out0 is None and out1 is None:
            pass
        elif out0 is None: # out1 is not None
            src1 = out1.src.pop()
            out1.dst.append('1')
            if   src1 == '0' and not in0reply.is_full():
                self.rep0 = out1
                out1reply.pop()
            elif src1 == '1' and not in1reply.is_full():
                self.rep1 = out1
                out1reply.pop()
            elif src1 == 'x'\
                    and not in0reply.is_full()\
                    and not in1reply.is_full():
                self.rep0 = out1
                self.rep1 = copy(out1)
                self.rep1.cycle = out1.cycle
                out1reply.pop()
            else:
                print "Channel full."
        elif out1 is None: # out0 is not None
            src0 = out0.src.pop()
            out0.dst.append('0')
            if   src0 == '0' and not in0reply.is_full():
                self.rep0 = out0
                out0reply.pop()
            elif src0 == '1' and not in1reply.is_full():
                self.rep1 = out0
                out0reply.pop()
            elif src0 == 'x'\
                    and not in0reply.is_full()\
                    and not in1reply.is_full():
                self.rep0 = out0
                self.rep1 = copy(out0)
                self.rep1.cycle = out0.cycle
                out0reply.pop()
            else:
                print "Channel full."
        else:
            src0 = out0.src.pop()
            src1 = out1.src.pop()
            if src0 == src1: # conflict, same adress
                #print "Conflict on reply (switch", self.id, ")"
                self.onConflict()

                if rand(0,1) == 0:
                    out0.dst.append('0')
                    if src0 == 'x'\
                            and not in0reply.is_full()\
                            and not in1reply.is_full():
                        self.rep0 = out0
                        self.rep1 = copy(out0)
                        self.rep1.cycle = out0.cycle
                        out0reply.pop()
                    elif src0 == '0' and not in0reply.is_full():
                        self.rep0 = out0
                        out0reply.pop()
                    elif src0 == '1' and not in1reply.is_full(): 
                        self.rep1 = out0
                        out0reply.pop()
                    else:
                        print "Channel full."
                else:
                    out1.dst.append('1')
                    if src1 == 'x'\
                            and not in0reply.is_full()\
                            and not in1reply.is_full():
                        self.rep0 = out1
                        self.rep1 = copy(out1)
                        self.rep1.cycle = out1.cycle
                        out1reply.pop()
                    elif src1 == '0' and not in0reply.is_full():
                        self.rep0 = out1
                        out1reply.pop()
                    elif src1 == '1' and not in1reply.is_full(): 
                        self.rep1 = out1
                        out1reply.pop()
                    else:
                        print "Channel full."
            elif src0 == 'x': # conflict, multicast
                #print "Conflict on multicast reply (switch", self.id, ")"
                self.onConflict()

                if rand(0,1) == 0\
                            and not in0reply.is_full()\
                            and not in1reply.is_full():
                    out0.dst.append('0')
                    self.rep0 = out0
                    self.rep1 = copy(out0)
                    self.rep1.cycle = out0.cycle
                    out0reply.pop()
                else:
                    out1.dst.append('1')
                    if   src1 == '0' and not in0reply.is_full():
                        self.rep0 = out1
                        out1reply.pop()
                    elif src1 == '1' and not in1reply.is_full(): 
                        self.rep1 = out1
                        out1reply.pop()
                    else:
                        print "Channel full."
            elif src1 == 'x': # conflict, multicast
                #print "Conflict on multicast reply (switch", self.id, ")"
                self.onConflict()

                if rand(0,1) == 1\
                            and not in0reply.is_full()\
                            and not in1reply.is_full():
                    out1.dst.append('1')
                    self.rep0 = out1
                    self.rep1 = copy(out1)
                    self.rep1.cycle = out1.cycle
                    out1reply.pop()
                else:
                    out0.dst.append('0')
                    if   src0 == '0' and not in0reply.is_full():
                        self.rep0 = out0
                        out0reply.pop()
                    elif src1 == '1' and not in1reply.is_full(): 
                        self.rep1 = out0
                        out0reply.pop()
                    else:
                        print "Channel full."
            else: # no conflict
                out0.dst.append('0')
                out1.dst.append('1')
                if src0 == '0': # src1 = '1'
                    if not in0reply.is_full():
                        self.rep0 = out0
                        out0reply.pop()
                    else:
                        print "Channel full."
                    if not in1reply.is_full():
                        self.rep1 = out1
                        out1reply.pop()
                    else:
                        print "Channel full."
                else: # src0 = '1' and src1 = '0'
                    if not in0reply.is_full():
                        self.rep0 = out1
                        out1reply.pop()
                    else:
                        print "Channel full."
                    if not in1reply.is_full():
                        self.rep1 = out0
                        out0reply.pop()
                    else:
                        print "Channel full."

    def clock2(self):
        """Propagate the messages. Second part of the clock cycle."""
        if self.req0 is not None:
            self.out0.request.write(self.req0)
            self.req0 = None

        if self.req1 is not None:
            self.out1.request.write(self.req1)
            self.req1 = None

        if self.rep0 is not None:
            self.in0.reply.write(self.rep0)
            self.rep0 = None

        if self.rep1 is not None:
            self.in1.reply.write(self.rep1)
            self.rep1 = None

#--------------------------------------------------------------------------------

class bus(component): pass

#--------------------------------------------------------------------------------

class simpleBus(bus):
    def __init__(self, arbiter_class, dst_len, src_len):
        component.__init__(self)
        self.message    = None
        self.address    = None
        self.dst_len    = dst_len
        self.src_len    = src_len
        self.requesting = []
        self.replying   = []
        self.waiting    = []
        self.arbiter    = arbiter_class()
        print "Simple bus", self.id

    def attach(self,obj,requesting=False):
        """Attaches an object to the bus."""
        if requesting:
            self.requesting.append(obj)
        else:
            self.replying.append(obj)

    def update_arbiter(self):
        """Tells the arbiter the objects attached"""
        self.arbiter.set(self.requesting + self.replying)

    def clock(self):
        """Executes one clock cycle"""
        # choose the device that will write on the bus
        eligible = [x for\
                x in self.replying\
                if len(x) > 0 \
                and x not in self.waiting]
        eligible += [x for\
                x in self.requesting\
                if len(x) > 0 \
                and (x.read().function != "load"
                     or x.read().dst not in self.waiting)
                ]
        chosen = self.arbiter.choose(eligible)

        if chosen in self.requesting:
            # obtain the message to transmit
            self.message = chosen.request.read()

            # append the address of the device it comes from
            src = bin(self.requesting.index(chosen), self.src_len)
            for c in reversed(src):
                self.message.src.append(c)

            # obtain the address of the device that should receive it
            self.address = ""
            for i in xrange(self.dst_len):
                self.address += self.message.dst.pop()

            # now that the message is ready, we try to transmit it
            try:
                self.replying[int(self.address,2)].request.write(message)
            except:
                return # too bad, try again some other time !

            # the message is transmitted, we can update the arbiter and
            # add the device to the waiting queue
            self.waiting.extend([x for x in self.requesting]) # TODO
        else:
            # appending
            src = bin(self.replying.index(chosen), self.dst_len)
            for c in reversed(src):
                self.message.dst.append(c)
            # obtain the address
            for i in xrange(self.dst_len):
                self.address += self.message.src.pop()

#--------------------------------------------------------------------------------

# a bus for requests, a bus for replies
class doubleBus(bus): pass

#--------------------------------------------------------------------------------

# a decorator of the class bus to implement a cache
class cachedBus(bus): pass

#--------------------------------------------------------------------------------

@circle
class processor(component):
    def __len__(self):
        # just an non-null value to enable unlimited run
        return 42

    def usage(self):
        return self.channel.reply.usage()

    def __init__(self,scene, x, y, p,nbits,channel = None,\
            boundRequest = None, boundReply = None, loadRatio = 1.7):
        """A processor with a probability p of requesting
        a word in memory."""
        assert 0 <= p <= 1
        assert isinstance(nbits,int)

        self.rand = Random()

        component.__init__(self)
        self.p = p
        self.loadRatio = loadRatio
        if channel is None:
            self.channel = channel = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(channel,channels.biChannel)
            self.channel = channel
        channel.setP(70*x+45, 70*y+25)

        self.nbits = nbits
        self.message = None
        self.num_instr = 0L
        print "Processor", self.id

    def address(self):
        return randbits(self.nbits)

    def produce(self):
        if randbool(self.p, self.rand):
            if randbool(1.0 / (1.0 + self.loadRatio), self.rand):
                function = "store"
            else:
                function = "load"
        else:
            function = None
        return function 

    def clock1(self):
        m = self.channel.reply.read()
        if m is None:
            return
        s = "Message from word %d arrived :%d" \
          % (int(''.join(m.dst), 2), simulator.cycle - m.cycle)
        print s
        self.channel.reply.pop()

    def clock2(self):
        if self.message is not None:
            try:
                self.channel.request.write(self.message)
                self.message = None
            except:
                pass
        else:
            function = self.produce()
            if function is None:
                return

            self.message = message.message([],self.address(), function ,
                    "", cycle=simulator.cycle)
            try:
                self.channel.request.write(self.message)
                self.message = None
            except:
                pass

class simpleSPMD(processor):
    seed = rand(0,maxint)

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
            s = "Message from word %d arrived :%d" \
                    % (int(''.join(m.dst), 2), simulator.cycle - m.cycle)
            print s
            self.channel.reply.pop()
            self.arrived.append(''.join(m.dst))
        except Exception as inst:
            print type(inst), inst, m.function
            raise inst

    def clock2(self):
        thread = self.threads[0]
        self.rand = thread.rand

        if len(self.threads) == 0:
            raise simulator.Finished()
        if  self.threads[0].waiting in self.arrived:
            self.arrived.remove(self.threads[0].waiting)
            self.threads[0].waiting = None
        elif self.threads[0].waiting is not None:
            print "Still awaiting reply from %s." %\
                    self.threads[0].waiting #int(self.threads[0].waiting,2))
            self.threads.append(self.threads[0])
            del self.threads[0]
            self.num_instr = 0
            return

        if self.message is None:
            function = self.produce()
            thread.rand = self.rand
            if function is None:
                return

            self.message = message.message([],self.address(), function ,
                    "", cycle=simulator.cycle)

        if not self.channel.request.is_full():
            self.channel.request.write(self.message)
            if self.message.function == "load":
                self.threads[0].waiting = ''.join(self.message.dst)
            if self.message.function == "load" or self.num_instr == self.batch_size:
                self.threads.append(self.threads[0])
                del self.threads[0]
                self.num_instr = 0
            self.message = None

        if len(self.threads) ==0:
            raise simulator.Finished()

#--------------------------------------------------------------------------------

@half_circle
class memory(component):
    def __init__(self,scene, x, y,\
            latency,channel = None, boundRequest = None, boundReply = None):
        assert isinstance(latency,int)
        component.__init__(self)
        if channel is None:
            channel = channels.biChannel(scene, boundRequest, boundReply)
        else:
            assert isinstance(channel,channels.biChannel)
        self.channel = channel

        channel.setP(70*x+5, 70*y+25)
        self.latency = latency
        self.buff = []
        print "Memory", self.id

    def usage(self):
        return self.channel.request.usage()

    def clock1(self):
        message = self.channel.request.read()
        if message is None:
            return

        self.buff[0:0] = [message] + ([None] * self.latency)
        self.channel.request.pop()

    def clock2(self):
        if len(self.buff) == 0:
            return
        message = self.buff[-1]
        if message is None:
            self.buff.pop()
        elif message.function == "load":
            message.to_memory = False
            try:
                self.channel.reply.write(message)
                self.buff.pop()
            except:
                pass
        else:
            self.buff.pop()
