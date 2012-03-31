from minijs.objects.base import W_Root


class W_BoolObject(W_Root):
    def __init__(self, boolval):
        self.boolval = boolval

    def bool(self, space):
        return self

    def bool_w(self, space):
        return self.boolval