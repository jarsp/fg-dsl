# Factor Graph DSL

This is a WIP DSL for describing factor graphs. gen\_lp.py generates the
(mixed) integer linear program corresponding to the energy minimization problem
(i.e. the MLE inference problem) over the factor graph and hands it over to the
Gurobi solver.

## Running

Requires: Python3, ANTLRv4, gurobi, gurobipy (for Python 3)  

In the parser subdirectory, run `make` to generate the parser.  

## Examples
Easy: python gen\_lp.py tests/easy.fg.

Wannacry: python gen\_lp.py tests/wannacry.fg  
You can use set and unset in the .fg file to set and unset variables. I might
tweak the weights assigned to set and unset variables in future. Things to try
include setting inf, setting exe, setting dns, and combinations of those.
