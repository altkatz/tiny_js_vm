from minijs.parser import Block, Stmt, Assignment, BinOp, Variable, ConstantFloat


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

    def test_multiple_statements(self, space):
        r = space.parse("""
        1 + 1;
        2 + 2;
        3 + 3;
        """)
        assert r == Block([
            Stmt(BinOp("+", ConstantFloat(1), ConstantFloat(1))),
            Stmt(BinOp("+", ConstantFloat(2), ConstantFloat(2))),
            Stmt(BinOp("+", ConstantFloat(3), ConstantFloat(3))),
        ])

    def test_variables(self, space):
        r = space.parse("""
        a = 3;
        a + 2;
        """)
        assert r == Block([
            Stmt(Assignment("a", ConstantFloat(3))),
            Stmt(BinOp("+", Variable("a"), ConstantFloat(2))),
        ])