from minijs import consts


class TestCompiler(object):
    def assert_compiles(self, space, source, expected_bytecode):
        bc = space.compile(source)
        expected = [
            line.strip()
            for line in expected_bytecode.splitlines()
            if line.strip()
        ]

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