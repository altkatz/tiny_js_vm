from minijs.parser import Block, Stmt, ConstantFloat


class TestParser(object):
    def test_const_float(self, space):
        assert space.parse("1") == Block([Stmt(ConstantFloat(1))])