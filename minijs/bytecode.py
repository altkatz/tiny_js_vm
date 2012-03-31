class Bytecode(object):
    def __init__(self, code, max_stackdepth, consts):
        self.code = code
        self.max_stackdepth = max_stackdepth
        self.consts = consts
