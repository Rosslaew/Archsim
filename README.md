# USAGE

The simulator runs a file containing a  description of an architecture,
for instance "arch.py" which uses components described in the files in
the folder "components".

There are two ways of executing arch.py, one with graphical visualization
and one without.

## Graphical mode

Command:
`./main.py graphical arch.py`

There is no option for this mode. A window representing the architecture as defined
in arch.py opens, and updates a each clock cycle, every second.

The color of a component describes the usage of the channels. If channels are empty,
the component is blue. When there are messages in the incoming channels,
the component becomes progressively red. The color is a gradient, analogous to
a number between 0 and 1 given by the method "usage".


## Command line mode

Command:
`./main.py cmdline arch.py`

Option: -n NUMBER
Limits the number of cycles of execution to at most NUMBER cycles.

In this mode, the architecture runs as fast as possible, only printing the result
on standard output.


## Statistics extraction

Command :
`./statistics.py <numbers>`

Options: -minx NUMBER, -maxx NUMBER
Sets the bounds for the graph

Extract statistics from the numbers given (mean, median, ...) and draws their
repartition.

Useful example : 
`./main.py cmdline arch.py | grep "arrived" | cut -d : -f 2 | ./statistics.py `

# DEVELOPMENT

## Adding a components library
1. Create the file in the "components" folder
2. Add it in simulator.py > instanciator > instanciate


# OBTAIN 

`git clone git://github.com/Rosslaew/Archsim.git`
