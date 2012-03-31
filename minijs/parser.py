import os

from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function

from minijs import consts


with open(os.path.join(os.path.dirname(__file__), "grammar.txt")) as f:
    grammar = f.read()
regexs, rules, _ = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)


class Node(object):
    _attrs_ = ()

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def compile(self, ctx):
        raise NotImplementedError(type(self).__name__)

class Block(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def compile(self, ctx):
        for stmt in self.stmts:
            stmt.compile(ctx)

class Stmt(Node):
    def __init__(self, expr):
        self.expr = expr

    def compile(self, ctx):
        self.expr.compile(ctx)
        ctx.emit(consts.DISCARD_TOP)

class Assignment(Node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def compile(self, ctx):
        self.expr.compile(ctx)
        ctx.emit(consts.STORE_NAME, ctx.create_name(self.var))

class If(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def compile(self, ctx):
        self.cond.compile(ctx)
        pos = ctx.get_pos()
        ctx.emit(consts.JUMP_IF_FALSE, 0)
        self.body.compile(ctx)
        ctx.patch_jump(pos)

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def compile(self, ctx):
        back_jump_target = ctx.get_pos()
        self.cond.compile(ctx)
        pos = ctx.get_pos()
        ctx.emit(consts.JUMP_IF_FALSE, 0)
        self.body.compile(ctx)
        ctx.emit(consts.JUMP, back_jump_target)
        ctx.patch_jump(pos)


class BinOp(Node):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def compile(self, ctx):
        self.lhs.compile(ctx)
        self.rhs.compile(ctx)
        ctx.emit(consts.BINOP_BYTECODE[self.op])

class Variable(Node):
    def __init__(self, var):
        self.var = var

    def compile(self, ctx):
        ctx.emit(consts.LOAD_NAME, ctx.create_name(self.var))

class ConstantFloat(Node):
    def __init__(self, floatval):
        self.floatval = floatval

    def compile(self, ctx):
        ctx.emit(consts.LOAD_CONST, ctx.create_float_const(self.floatval))


class Transformer(object):
    def visit_main(self, node):
        return self.visit_block(node.children[0])

    def visit_block(self, node):
        stmts = []
        while True:
            stmts.append(self.visit_stmt(node.children[0]))
            if len(node.children) == 1:
                break
            node = node.children[1]
        return Block(stmts)

    def visit_stmt(self, node):
        if node.children[0].symbol == "expr":
            return Stmt(self.visit_expr(node.children[0]))

        info = node.children[0].additional_info
        if info == "if":
            return self.visit_if(node)
        elif info == "while":
            return self.visit_while(node)
        raise NotImplementedError

    def visit_if(self, node):
        return If(
            self.visit_expr(node.children[2]),
            self.visit_block(node.children[5]),
        )

    def visit_while(self, node):
        return While(
            self.visit_expr(node.children[2]),
            self.visit_block(node.children[5]),
        )

    def visit_expr(self, node):
        if node.symbol == "expr":
            node = node.children[0]

        symname = node.symbol
        if symname == "assignment":
            return self.visit_assignment(node)
        elif symname in ["additive", "multitive", "comparison"]:
            return self.visit_subexpr(node)
        elif symname == "primary":
            return self.visit_primary(node)
        raise NotImplementedError

    def visit_subexpr(self, node):
        if len(node.children) == 1:
            return self.visit_expr(node.children[0])
        return BinOp(
            node.children[1].additional_info,
            self.visit_expr(node.children[0]),
            self.visit_expr(node.children[2]),
        )
        raise NotImplementedError

    def visit_assignment(self, node):
        return Assignment(
            node.children[0].additional_info,
            self.visit_expr(node.children[2])
        )

    def visit_primary(self, node):
        if len(node.children) == 1:
            return self.visit_atom(node.children[0])
        elif node.children[0].additional_info == "(":
            return self.visit_expr(node.children[1])
        raise NotImplementedError

    def visit_atom(self, node):
        symname = node.children[0].symbol
        if symname == "FLOAT":
            return ConstantFloat(float(node.children[0].additional_info))
        elif symname == "NAME":
            return Variable(node.children[0].additional_info)
        raise NotImplementedError