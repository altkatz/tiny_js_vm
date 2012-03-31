from minijs.parser import Block, Stmt, BinOp, ConstantFloat


class TestParser(object):
    def test_const_float(self, space):
        assert space.parse("1;") == Block([Stmt(ConstantFloat(1))])

    def test_binary_expressions(self, space):
        assert space.parse("1 + 1;") == Block([Stmt(BinOp("+", ConstantFloat(1), ConstantFloat(1)))])
        assert space.parse("2 - 3;") == Block([Stmt(BinOp("-", ConstantFloat(2), ConstantFloat(3)))])

    def test_multi_term_expr(self, space):
        assert space.parse("1 - 2 * 3;") == Block([Stmt(BinOp("-", ConstantFloat(1), BinOp("*", ConstantFloat(2), ConstantFloat(3))))])

    def test_comparisons(self, space):
        assert space.parse("1 > 2;") == Block([Stmt(BinOp(">", ConstantFloat(1), ConstantFloat(2)))])

