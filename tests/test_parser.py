from minijs.parser import (Block, Stmt, If, While, Print, Assignment, BinOp,
    Variable, ConstantFloat)


class TestParser(object):
    def test_const_float(self, space):
        assert space.parse("1;") == Block([Stmt(ConstantFloat(1))])

    def test_binary_expressions(self, space):
        assert space.parse("1 + 1;") == Block([Stmt(BinOp("+", ConstantFloat(1), ConstantFloat(1)))])
        assert space.parse("2 - 3;") == Block([Stmt(BinOp("-", ConstantFloat(2), ConstantFloat(3)))])

    def test_multi_term_expr(self, space):
        assert space.parse("1 - 2 * 3;") == Block([Stmt(BinOp("-", ConstantFloat(1), BinOp("*", ConstantFloat(2), ConstantFloat(3))))])

    def test_parens(self, space):
        assert space.parse("(1 - 2) * 3;") == Block([Stmt(BinOp("*", BinOp("-", ConstantFloat(1), ConstantFloat(2)), ConstantFloat(3)))])

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

    def test_if(self, space):
        r = space.parse("""
        if (2) {
            a = 4;
        }
        """)
        assert r == Block([
            If(ConstantFloat(2),
                Block([
                    Stmt(Assignment("a", ConstantFloat(4))),
                ])
            ),
        ])

    def test_while(self, space):
        r = space.parse("""
        i = 0;
        while (i < 10) {
            i = i + 1;
        }
        """)
        assert r == Block([
            Stmt(Assignment("i", ConstantFloat(0))),
            While(
                BinOp("<", Variable("i"), ConstantFloat(10)),
                Block([
                    Stmt(Assignment("i", BinOp("+", Variable("i"), ConstantFloat(1))))
                ])
            ),
        ])

    def test_print(self, space):
        assert space.parse("print 3;") == Block([Print(ConstantFloat(3))])