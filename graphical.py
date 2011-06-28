from PyQt4        import QtCore,QtGui
from PyQt4.QtCore import Qt, QLineF, QRectF, QPointF
from PyQt4.QtGui  import QGraphicsLineItem, QGraphicsRectItem, QGraphicsEllipseItem


class QGraphicsHalfCircle(QGraphicsEllipseItem):
    def __init__(self, *args, **kwords):
        QGraphicsEllipseItem.__init__(self, *args, **kwords)
        self.setSpanAngle(180*16)
        
def graphicalComponent(QtClass):
    def decorator(comp):
        class wrapper(comp, QtClass):
            def __init__(self, scene, x, y, *args, **kwords):
                comp.__init__(self, scene, x, y, *args, **kwords)
                QtClass.__init__(self, 70*x+5., 70*y+5., 40., 40., scene = scene)

                pen = QtGui.QPen()
                pen.setWidth(1)
                pen.setStyle(Qt.SolidLine)

                self.setPen(pen)
                self.update_color()

            def clock2(self):
                comp.clock2(self)
                self.update_color()

            def update_color(self):
                color = QtGui.QColor()
                color.setHsvF((1. - self.usage())*240./360., 1., 1.)

                pen = self.pen()
                pen.setBrush(color)
                self.setPen(pen)
        return wrapper
    return decorator

circle      = graphicalComponent(QGraphicsEllipseItem)
half_circle = graphicalComponent(QGraphicsHalfCircle)
rectangle   = graphicalComponent(QGraphicsRectItem)

def segment(comp):
    class wrapper(comp, QGraphicsLineItem):
        def __init__(self, scene, *args, **kwords):
            comp.__init__(self, *args, **kwords)
            QGraphicsLineItem.__init__(self,QLineF(), scene = scene)

            pen = QtGui.QPen()
            pen.setWidth(1)
            pen.setBrush(Qt.black)
            pen.setStyle(Qt.NoPen)

            self.setPen(pen)
            self.nextPoint = 1

        def setP(self,x, y):
            pos = QPointF(x,y)
            if self.nextPoint == 1:
                l = self.line()
                l.setP1(pos)
                self.setLine(l)
                self.nextPoint = 2
            else:
                pen = self.pen()
                pen.setStyle(Qt.SolidLine)
                self.setPen(pen)

                l = self.line()
                l.setP2(pos)
                self.setLine(l)
                self.nextPoint = 1
    return wrapper

#class qSimpleSwitch(simpleSwitch, QGraphicsRectItem):
#    def __init__(self, scene, x, y,\
#            in0=None,\
#            in1=None,\
#            out0=None,\
#            out1 = None,\
#            boundRequest = None,\
#            boundReply = None,\
#            onConflict = None):
#
#
#        simpleSwitch.__init__(self, in0, in1, out0, out1, boundRequest, boundReply, onConflict)
#        QGraphicsRectItem.__init__(self, 80*x+5, 60*y+5, 40, 50, scene = scene)
#
#        pen = QtGui.QPen()
#        pen.setWidth(1)
#        pen.setStyle(Qt.SolidLine)
#
#        self.setPen(pen)
#        self.update_color()
#
#
#
#class qProcessor(processor, QGraphicsEllipseItem):
#    def __init__(self, scene, x, y, p, nbits,\
#            channel = None, boundRequest = None, boundReply = None):
#        if channel == None:
#            channel = qBiChannel(scene, boundRequest, boundReply)
#        else:
#            assert isinstance(channel,qBiChannel)
#        channel.setP(80*x+45, 60*y+25)
#
#        processor.__init__(self, p, nbits, channel, boundRequest, boundReply)
#        QGraphicsEllipseItem.__init__(self, 80*x+5, 60*y+5, 40, 40, scene = scene)
#
#        pen = QtGui.QPen()
#        pen.setWidth(1)
#        pen.setStyle(Qt.SolidLine)
#
#        self.setPen(pen)
#        self.update_color()
#
#
#class qSimpleSPMD(simpleSPMD, QGraphicsEllipseItem):
#    def __init__(self, scene, x, y, ninstr, nthreads, p, nbits,\
#            batch_size = float("infinity"), loop = True,\
#            channel = None, boundRequest = None, boundReply = None):
#        if channel == None:
#            channel = qBiChannel(scene, boundRequest, boundReply)
#        else:
#            assert isinstance(channel,qBiChannel)
#
#        simpleSPMD.__init__(self, ninstr, nthreads, batch_size, loop,\
#                p, nbits, channel, boundRequest, boundReply)
#        QGraphicsEllipseItem.__init__(self, 80*x+5, 60*y+5, 40, 40, scene = scene)
#
#        pen = QtGui.QPen()
#        pen.setWidth(1)
#        pen.setStyle(Qt.SolidLine)
#
#        self.setPen(pen)
#        self.update_color()
#
#class qMemory(memory, QGraphicsEllipseItem):
#    def __init__(self, scene, x, y, latency, channel = None, boundRequest = None, boundReply = None):
#        QGraphicsEllipseItem.__init__(self, 80*x+5, 60*y+5, 40, 40, scene = scene)
#
#        self.setSpanAngle(180*16)
#
#        pen = QtGui.QPen()
#        pen.setWidth(1)
#        pen.setStyle(Qt.SolidLine)
#
#        self.setPen(pen)
#        self.update_color()
#
