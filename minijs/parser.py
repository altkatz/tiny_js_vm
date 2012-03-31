import os

from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function


with open(os.path.join(os.path.dirname(__file__), "grammar.txt")) as f:
    grammar = f.read()
regexs, rules, _ = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)


class Node(object):
    _attrs_ = ()

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

class Block(Node):
    def __init__(self, stmts):
        self.stmt = stmts

class Stmt(Node):
    def __init__(self, expr):
        self.expr = expr

class ConstantFloat(Node):
    def __init__(self, floatval):
        self.floatval = floatval


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
        raise NotImplementedError

    def visit_expr(self, node):
        if node.symbol == "expr":
            node = node.children[0]
        if node.symbol == "comparison":
            return self.visit_subexpr(node)
        elif node.symbol == "primary":
            return self.visit_primary(node)
        raise NotImplementedError

    def visit_subexpr(self, node):
        if len(node.children) == 1:
            return self.visit_expr(node.children[0])
        raise NotImplementedError

    def visit_primary(self, node):
        if len(node.children) == 1:
            return self.visit_atom(node.children[0])
        raise NotImplementedError

    def visit_atom(self, node):
        if node.children[0].symbol == "FLOAT":
            return ConstantFloat(float(node.children[0].additional_info))