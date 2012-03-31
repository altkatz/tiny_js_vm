class Bytecode(object):
    def __init__(self, code, max_stackdepth, consts, names):
        self.code = code
        self.max_stackdepth = max_stackdepth
        self.consts = consts
        self.names = names
