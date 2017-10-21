from typing import List, Dict

class FGAst:
    pass

class FGModule(FGAst):
    def __init__(self, name:str, defs:Dict[str, 'FGDef'], apps:List['FGApp']) -> None:
        self.name = name
        self.defs = defs
        self.apps = apps
        self.variables = set()
        for app in apps: self.variables.update(app.args)
    def __str__(self) -> str:
        s = 'FGModule {}:\n'.format(self.name)
        s += 'Defs:\n'
        for d in self.defs.values():
            s += '\t' + str(d) + '\n'
        s += 'Apps:\n'
        for a in self.apps:
            s += '\t' + str(a) + '\n'
        return s

class FGDef(FGAst):
    def __init__(self, name:str, params:List['FGVar'], exp:'FGExp') -> None:
        self.name = name
        self.params = params
        self.exp = exp
    def __str__(self) -> str:
        s = self.name + '\t' + ', '.join(map(str, self.params)) + '\t' + str(self.exp)
        return s

class FGApp(FGAst):
    def __init__(self, name:str, args:List['FGVar']) -> None:
        self.name = name
        self.args = args
    def __str__(self) -> str:
        s = self.name + '\t' + ', '.join(map(str, self.args))
        return s

class FGExp(FGAst):
    def __init__(self, expr:'FGExp') -> None:
        self.expr = expr
    def __str__(self) -> str:
        return str(self.expr)

class FGOp(FGExp):
    __OPS = {
        'neg': ('-', 1, lambda a: -a),
        'add': ('+', 2, lambda a, b: a + b),
        'sub': ('-', 2, lambda a, b: a - b),
        'mul': ('*', 2, lambda a, b: a * b),
        'div': ('/', 2, lambda a, b: a / b),
        'pow': ('^', 2, lambda a, b: a ** b)
    }

    def __init__(self, opname:str, args:List['FGExp']) -> None:
        self.symbol, self.arity, self.fn = self.__OPS[opname]
        self.opname = opname
        self.args = args
    def __str__(self) -> str:
        argstr = ' '.join(list(map(str, self.args)))
        s = '(' + self.symbol + ' ' + argstr + ')'
        return s

class FGVar(FGExp):
    def __init__(self, name:str) -> None:
        self.name = name
    def __str__(self) -> str:
        s = 'Var({})'.format(self.name)
        return s

class FGConst(FGExp):
    def __init__(self, value:float) -> None:
        self.value = value
    def __str__(self) -> str:
        s = 'Const({})'.format(self.value)
        return s
