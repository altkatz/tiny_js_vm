from minijs import consts


class Frame(object):
    def __init__(self, bytecode):
        self.stack = [None] * bytecode.max_stackdepth
        self.locals_w = [None] * len(bytecode.names)
        self.stackpos = 0

    def push(self, w_obj):
        self.stack[self.stackpos] = w_obj
        self.stackpos += 1

    def pop(self):
        stackpos = self.stackpos - 1
        w_res = self.stack[stackpos]
        self.stackpos = stackpos
        return w_res

    def peek(self):
        return self.stack[self.stackpos - 1]


class Interpreter(object):
    def interpret(self, space, frame, bytecode):
        pc = 0
        while True:
            instr = ord(bytecode.code[pc])
            pc += 1
            args = ()
            for i in xrange(consts.BYTECODE_NUM_ARGS[instr]):
                args += (ord(bytecode.code[pc]),)
                pc += 1

            if instr == consts.RETURN_NULL:
                assert frame.stackpos == 0
                return None

            method = getattr(self, consts.BYTECODE_NAMES[instr])
            res = method(space, bytecode, frame, pc, *args)
            if res is not None:
                pc = res

    def LOAD_CONST(self, space, bytecode, frame, pc, idx):
        frame.push(bytecode.consts[idx])

    def LOAD_NAME(self, space, bytecode, frame, pc, idx):
        frame.push(frame.locals_w[idx])

    def STORE_NAME(self, space, bytecode, frame, pc, idx):
        frame.locals_w[idx] = frame.peek()

    def _new_binop(opname):
        def impl(self, space, bytecode, frame, pc):
            w_rhs = frame.pop()
            w_lhs = frame.pop()
            method = getattr(space, opname)
            return frame.push(method(w_lhs, w_rhs))
        impl.__name__ = "BINARY_%s" % opname.upper()
        return impl
    BINARY_SUB = _new_binop("sub")
    BINARY_GE = _new_binop("ge")


    def PRINT_ITEM(self, space, bytecode, frame, pc):
        w_obj = frame.pop()
        self.print_(space.str_w(space.str(w_obj)))

    def JUMP(self, space, bytecode, frame, pc, target_pc):
        return target_pc

    def JUMP_IF_FALSE(self, space, bytecode, frame, pc, target_pc):
        w_obj = frame.pop()
        if space.bool_w(space.bool(w_obj)):
            return pc
        return target_pc

    def DISCARD_TOP(self, space, bytecode, frame, pc):
        frame.pop()