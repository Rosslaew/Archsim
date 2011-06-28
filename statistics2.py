#!/usr/bin/python2
from sys import stdin,exit
import scipy.stats as stats
import numpy

ncycles = [int(n) for n in stdin]

if len(ncycles) == 0:
    print "I need data !"
    exit()

def mode(l):
    return max([(l.count(i),i) for i in frozenset(l)])[1]

print "Moyenne  :", numpy.mean(ncycles)
print "Mediane  :", sorted(ncycles)[len(ncycles)//2]
print "Maximum  :", max(ncycles)
print "Minimum  :", min(ncycles)
print "Variance :", numpy.var(ncycles)
print "Mode     :", mode(ncycles)
