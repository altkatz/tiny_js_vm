class W_Root(object):
    _attrs_ = ()

    def str(self, space):
        raise NotImplementedError
    def str_w(self, space):
        raise NotImplementedError