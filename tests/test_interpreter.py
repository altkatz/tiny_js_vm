from minijs.interpreter import Interpreter


class MockInterpreter(Interpreter):
    def __init__(self, *args, **kwargs):
        super(MockInterpreter, self).__init__(*args, **kwargs)
        self._output = []

    def print_(self, value):
        self._output.append(value)



class TestInterpreter(object):
    space_options = {
        "interpreter_cls": MockInterpreter,
    }

    def run(self, space, source):
        space.exec_(source)
        return space.interpreter._output

    def test_simple(self, space):
        output = self.run(space, "x = 3; print x;")
        assert output == ["3.0"]

    def test_while_loop(self, space):
        output = self.run(space, """
        i = 3;
        while (i >= 0) {
            print i;
            i = i - 1;
        }
        """)
        assert output == ["3.0", "2.0", "1.0", "0.0"]