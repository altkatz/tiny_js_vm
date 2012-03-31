from minijs import consts
from minijs.bytecode import Bytecode


class CompilerContext(object):
    def __init__(self, space):
        self.space = space
        self.data = []
        self.consts = []
        self.names = {}

    def emit(self, bc, *args):
        self.data.append(chr(bc))
        for arg in args:
            self.data.append(chr(arg))

    def create_name(self, name):
        if name not in self.names:
            self.names[name] = len(self.names)
        return self.names[name]

    def create_float_const(self, floatval):
        pos = len(self.consts)
        self.consts.append(self.space.newfloat(floatval))
        return pos

    def create_bytecode(self):
        bcs = "".join(self.data)
        max_stackdepth = self.count_stackdepth(bcs)
        return Bytecode(bcs, max_stackdepth, self.consts)

    def count_stackdepth(self, bc):
        i = 0
        current_stackdepth = 0
        max_stackdepth = 0
        while i < len(bc):
            c = ord(bc[i])
            i += 1
            stack_effect = consts.BYTECODE_STACK_EFFECT[c]
            i += consts.BYTECODE_NUM_ARGS[c]
            current_stackdepth += stack_effect
            max_stackdepth = max(current_stackdepth, max_stackdepth)
        return max_stackdepth