# Factor Graph DSL

This is a WIP DSL for describing factor graphs. gen\_lp.py generates the
(mixed) integer linear program corresponding to the energy minimization problem
(i.e. the MLE inference problem) over the factor graph and hands it over to the
Gurobi solver.

## Running

Requires: Python3, ANTLRv4, gurobi, gurobipy (for Python 3)  

In the parser subdirectory, run `make` to generate the parser.  
Try running python gen\_lp.py tests/easy.fg.

## Contributors

Benjamin Lim (jarsp)
