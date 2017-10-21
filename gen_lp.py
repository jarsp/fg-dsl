from parser import *
from gurobipy import *

import os
import sys
import itertools
import numpy as np

# Disable annoying log
TEMP_LOG='./gurobi.log'
setParam('LogFile', TEMP_LOG)

class DegenFGError(Exception):
    pass

# TODO: Simpler indexing perhaps
# TODO: Number of redundant constraints, but really I think Gurobi handles
#       those well, and this is easier to understand
def gen_lp(mod:FGModule) -> Model:
    m = Model("FG")

    # Individual indicator variables
    vs0 = [v + '0' for v in mod.variables]
    vs1 = [v + '1' for v in mod.variables]
    iv = m.addVars(vs0 + vs1, vtype=GRB.BINARY, name='iv')

    # Indicator constraint
    m.addConstrs((iv[v[0]] + iv[v[1]] == 1.0 for v in zip(vs0, vs1)))

    obj = 0.0
    for n, app in enumerate(mod.apps):
        # Pairwise indicator variables
        nargs = len(app.args)
        ivv = m.addVars(itertools.product((0.0, 1.0), repeat=len(app.args)),
                        vtype=GRB.BINARY,
                        name='ivv_' + str(n))

        # Indicator constraint
        any_ivv = ['*'] * nargs
        m.addConstr(ivv.sum(*any_ivv) == 1.0)

        # Consistency constraints
        for i, v in enumerate(app.args):
            fixv0_ivv = any_ivv[:i] + [0] + any_ivv[i+1:]
            fixv1_ivv = any_ivv[:i] + [1] + any_ivv[i+1:]
            m.addConstr(ivv.sum(*fixv0_ivv) == iv[v.name + '0'])
            m.addConstr(ivv.sum(*fixv1_ivv) == iv[v.name + '1'])

        # Calculate part of objective
        fdef = mod.defs[app.name]
        with np.errstate(divide='raise'):
            try:
                coeffs = {t: np.log(fdef(*t))
                          for t in itertools.product((0.0, 1.0),
                                                     repeat=len(app.args))}
            except FloatingPointError:
                raise DegenFGError('Factor is bad or evaluates to 0')
        obj += ivv.prod(coeffs)

    # Set objective
    m.update()
    m.setObjective(obj, GRB.MINIMIZE)
    m.update()

    return vs1, m

if __name__ == '__main__':
    module = parse_file(sys.argv[1])
    vs, model = gen_lp(module)
    model.optimize()
    if model.status == GRB.Status.OPTIMAL:
        print('================================')
        print(module)
        print('================================')
        print('Discovered solution:')
        for v1 in vs:
            print(model.getVarByName('iv[{}]'.format(v1)))
        print('================================')
        print('All variables:')
        for v in model.getVars():
            print(v)

    os.remove(TEMP_LOG)
