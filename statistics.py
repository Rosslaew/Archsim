#!/usr/bin/python2
from __future__ import division
from sys import stdin,exit
from matplotlib import pyplot as plt
import argparse

def main(args):
    ncycles = [int(n) for n in stdin]

    if len(ncycles) == 0:
        print "I need data !"
        exit()

    moyenne = sum(ncycles)/len(ncycles)

    print "Moyenne  :", moyenne
    print "Mediane  :", sorted(ncycles)[len(ncycles)//2]
    print "Maximum  :", max(ncycles)
    print "Minimum  :", min(ncycles)
    print "Variance :", sum([(n - moyenne)**2 for n in ncycles])/len(ncycles)

    fig = plt.figure()

    upper = fig.add_subplot(211)
    lower = fig.add_subplot(212)

    upper.hist(ncycles, sorted(list(set(ncycles))))
    lower.boxplot(ncycles, vert=0)

    if (args.minx, args.maxx) == (None,None):
        pass
    elif args.minx is None:
        fig.axes[0].set_xbound(None, int(args.maxx))
    elif args.minx is None:
        fig.axes[0].set_xbound(int(args.minx), None)
    else:
        fig.axes[0].set_xbound(int(args.minx),int(args.maxx))
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("A little tool to extract some statistics.")
    parser.add_argument("-minx", action = "store", default=None, help = "Minimum value")
    parser.add_argument("-maxx", action = "store", default=None, help = "Maximum value")
    args = parser.parse_args()
    main(args)

#    import argparse
#    parser = argparse.ArgumentParser(
#        description="""Architecture simulator.
#Uses a description of the architecture in Python.""")
#    subparsers = parser.add_subparsers()
#
#    cmdline = subparsers.add_parser('cmdline',
#            help = "Runs the program without a graphical interface.")
#
#    cmdline.add_argument(
#            "-n",
#            action = "store",
#            dest = "ncycles",
#            help = "Number of cycles to run (default : infinity)",
#            default = None)
#
#    cmdline.add_argument(
#            "file",
#            action = "store",
#            help = "Architecture description.")
#
#    graphical = subparsers.add_parser('graphical',
#            help = "Displays the network in a graphical interface (requires PyQt)")
#
#    graphical.add_argument(
#            "file",
#            action = "store",
#            help = "Architecture description.")
#
#    cmdline.set_defaults(func=main)
#    graphical.set_defaults(func=qMain)
#    args = parser.parse_args()
#    args.func(args)
