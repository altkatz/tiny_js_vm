import os

from pypy.rlib.parsing.ebnfparse import parse_ebnf


grammar = os.path.join(os.path.dirname(__file__), "grammar.txt")
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
    pass