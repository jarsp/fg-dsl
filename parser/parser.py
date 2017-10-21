from typing import Tuple

import sys

from antlr4 import *
from .FGLexer import FGLexer
from .FGVisitor import FGVisitor
from .FGParser import FGParser

from .ast import *

class FGTreeParse(FGVisitor):
    __expr_ops = {
        '+': 'add',
        '-': 'sub',
    }
    __term_ops = {
        '*': 'mul',
        '/': 'div',
    }
    __factor_ops = {
        '^': 'pow',
    }
    __signed_ops = {
        '-': 'neg',
    }

    # Visit a parse tree produced by FGParser#module.
    def visitModule(self, ctx:FGParser.ModuleContext) -> FGModule:
        name = ctx.variable().getText()
        defs = dict(map(self.visitFact_def, ctx.fact_def()))
        apps = list(map(self.visitFact_app, ctx.fact_app()))
        return FGModule(name, defs, apps)

    # Visit a parse tree produced by FGParser#fact_def.
    def visitFact_def(self, ctx:FGParser.Fact_defContext) -> Tuple[str, FGDef]:
        name = ctx.variable(0).getText()
        params = list(map(self.visitVariable, ctx.variable()[1:]))
        exp = self.visitExpression(ctx.expression())
        return (name, FGDef(name, params, exp))

    # Visit a parse tree produced by FGParser#fact_app.
    def visitFact_app(self, ctx:FGParser.Fact_appContext) -> FGApp:
        name = ctx.variable(0).getText()
        args = list(map(self.visitVariable, ctx.variable()[1:]))
        return FGApp(name, args)

    # Visit a parse tree produced by FGParser#expression.
    def visitExpression(self, ctx:FGParser.ExpressionContext) -> FGExp:
        # NOTE: A bit fragile? Same as the below
        ops = [self.__expr_ops[o.getText()] \
                for i, o in enumerate(ctx.getChildren()) \
                if i % 2 == 1]
        args = list(map(self.visitTerm, ctx.term()))
        ret = args[0]
        for o, a in zip(ops, args[1:]):
            ret = FGOp(o, [ret, a])
        return FGExp(ret)

    # Visit a parse tree produced by FGParser#term.
    def visitTerm(self, ctx:FGParser.TermContext) -> FGExp:
        ops = [self.__term_ops[o.getText()] \
                for i, o in enumerate(ctx.getChildren()) \
                if i % 2 == 1]
        args = list(map(self.visitFactor, ctx.factor()))
        ret = args[0]
        for o, a in zip(ops, args[1:]):
            ret = FGOp(o, [ret, a])
        return ret

    # Visit a parse tree produced by FGParser#factor.
    def visitFactor(self, ctx:FGParser.FactorContext) -> FGExp:
        ops = [self.__factor_ops[o.getText()] \
                for i, o in enumerate(ctx.getChildren()) \
                if i % 2 == 1]
        args = list(map(self.visitSignedAtom, ctx.signedAtom()))
        # Folding right
        ret = args[-1]
        for o, a in zip(reversed(ops), reversed(args[:-1])):
            ret = FGOp(o, [a, ret])
        return ret

    # Visit a parse tree produced by FGParser#signedAtom.
    def visitSignedAtom(self, ctx:FGParser.SignedAtomContext) -> FGExp:
        pos = True
        cur = ctx
        while cur.signedAtom() != None:
            if cur.MINUS() != None: pos = not pos
            cur = cur.signedAtom()
        res = self.visitAtom(cur.atom())
        if pos: return res
        else: return FGOp('neg', [res])

    # Visit a parse tree produced by FGParser#atom.
    def visitAtom(self, ctx:FGParser.AtomContext) -> FGExp:
        if ctx.scientific() != None: return self.visitScientific(ctx.scientific())
        if ctx.variable() != None: return self.visitVariable(ctx.variable())
        return self.visitExpression(ctx.expression())

    # Visit a parse tree produced by FGParser#scientific.
    def visitScientific(self, ctx:FGParser.ScientificContext) -> FGConst:
        return FGConst(float(ctx.getText()))

    # Visit a parse tree produced by FGParser#variable.
    def visitVariable(self, ctx:FGParser.VariableContext) -> FGVar:
        return FGVar(ctx.getText())

def parse_file(fname:str) -> FGModule:
    """
    Parses a .fg file into a FGModule.

    Args:
        fname: Name of file to parse.

    Returns:
        Parsed FGModule.
    """
    lexer = FGLexer(FileStream(fname))
    stream = CommonTokenStream(lexer)
    parser = FGParser(stream)
    tree = parser.module()
    tree_parser = FGTreeParse()
    return tree_parser.visitModule(tree)
