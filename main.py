#!/usr/bin/env python2
import sys

from PyQt4 import QtCore,QtGui, QtOpenGL

from components import base
from channels   import biChannel
from qSimulator import Ui_MainWindow
from simulator  import runner, instanciator

class qInstanciator(instanciator):
    def __init__(self, scene):
        instanciator.__init__(self)
        self.scene = scene

    def make(self,file):
        self.components = {}
        self.ncomponents = {}
        glob = globals()
        glob['scene'] = self.scene
        glob['self'] = self
        execfile(file, glob, locals())

# Create a class for our main window
class qRunner(runner, QtGui.QMainWindow):
    def __init__(self, file = None):
        runner.__init__(self, [])
        QtGui.QMainWindow.__init__(self)

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Since the UI is a QGraphicsView, I create a Scene
        # so it has something to show
        self.scene = QtGui.QGraphicsScene()
        self.ui.view.setScene(self.scene)



        # This makes the view OpenGL-accelerated. Usually makes
        # things much faster, but it *is* optional.

        self.ui.view.setViewport(QtOpenGL.QGLWidget())
        self.populate(file)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Create a timer
        self.animator=QtCore.QTimer()

        # And when it triggers, it calls the animate method
        self.animator.timeout.connect(self.clock)

        # And I animate it once manually.
        self.animator.start(1000)

    def clock(self):
        runner.clock(self)
        for c in self.components:
            c.update_color()

    def populate(self, file):
        inst = qInstanciator(self.scene)
        inst.make(file)
        self.components = inst.get_components()

def qMain(args):
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window = qRunner(args.file)

    window.show()

    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

def main(args):
    inst = qInstanciator(None)
    inst.make(args.file)
    run  = runner(inst.get_components())
    if args.ncycles is None:
        run.run()
    else:
        run.run(int(args.ncycles))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="""Architecture simulator.
Uses a description of the architecture in Python.""")
    subparsers = parser.add_subparsers()

    cmdline = subparsers.add_parser('cmdline',
            help = "Runs the program without a graphical interface.")

    cmdline.add_argument(
            "-n",
            action = "store",
            dest = "ncycles",
            help = "Number of cycles to run (default : infinity)",
            default = None)

    cmdline.add_argument(
            "file",
            action = "store",
            help = "Architecture description.")

    graphical = subparsers.add_parser('graphical',
            help = "Displays the network in a graphical interface (requires PyQt)")

    graphical.add_argument(
            "file",
            action = "store",
            help = "Architecture description.")

    cmdline.set_defaults(func=main)
    graphical.set_defaults(func=qMain)
    args = parser.parse_args()
    args.func(args)
