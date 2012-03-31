from minijs import consts


class TestCompiler(object):
    def assert_compiles(self, space, source, expected_bytecode):
        bc = space.compile(source)
        expected = []
        for line in expected_bytecode.splitlines():
            if "#" in line:
                line = line[:line.index("#")]
            line = line.strip()
            if line:
                expected.append(line)

        actual = []
        i = 0
        while i < len(bc.code):
            c = ord(bc.code[i])
            line = consts.BYTECODE_NAMES[c]
            i += 1
            for j in xrange(consts.BYTECODE_NUM_ARGS[c]):
                line += " %s" % ord(bc.code[i])
                i += 1
            actual.append(line)
        assert actual == expected
        return bc

    def test_assignment(self, space):
        bc = self.assert_compiles(space, "a = 3;", """
        LOAD_CONST 0
        STORE_NAME 0
        DISCARD_TOP
        RETURN_NULL
        """)
        [c] = bc.consts
        assert c.floatval == 3
        assert bc.max_stackdepth == 1

    def test_addition(self, space):
        self.assert_compiles(space, "a + 2;", """
        LOAD_NAME 0
        LOAD_CONST 0
        BINARY_ADD
        DISCARD_TOP
        RETURN_NULL
        """)

    def test_binops(self, space):
        self.assert_compiles(space, "(2 * 4) - (3 / 4);", """
        LOAD_CONST 0
        LOAD_CONST 1
        BINARY_MUL
        LOAD_CONST 2
        LOAD_CONST 1
        BINARY_DIV
        BINARY_SUB
        DISCARD_TOP
        RETURN_NULL
        """)

    def test_if(self, space):
        self.assert_compiles(space, "if (3) { 2 + 2; }", """
        LOAD_CONST 0
        JUMP_IF_FALSE 10
        LOAD_CONST 1
        LOAD_CONST 1
        BINARY_ADD
        DISCARD_TOP
        RETURN_NULL
        """)

    def test_while(self, space):
        self.assert_compiles(space, """
        i = 0;
        while (i < 10) {
            i = i + 1;
        }
        """, """
        LOAD_CONST 0
        STORE_NAME 0
        DISCARD_TOP
        LOAD_NAME 0
        LOAD_CONST 1
        BINARY_LT
        JUMP_IF_FALSE 22
        LOAD_NAME 0
        LOAD_CONST 2
        BINARY_ADD
        STORE_NAME 0
        DISCARD_TOP
        JUMP 5
        RETURN_NULL
        """)

    def test_print(self, space):
        self.assert_compiles(space, "print 3;", """
        LOAD_CONST 0
        PRINT_ITEM
        RETURN_NULL
        """)