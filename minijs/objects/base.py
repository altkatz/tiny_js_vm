class W_Root(object):
    _attrs_ = ()

    def float_w(self, space):
        raise NotImplementedError
    def bool(self, space):
        raise NotImplementedError
    def bool_w(self, space):
        raise NotImplementedError
    def str(self, space):
        raise NotImplementedError
    def str_w(self, space):
        raise NotImplementedError

    def sub(self, space, w_other):
        raise NotImplementedError
    def ge(self, space, w_other):
        raise NotImplementedError