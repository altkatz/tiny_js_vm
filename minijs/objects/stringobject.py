from minijs.objects.base import W_Root


class W_StringObject(W_Root):
    def __init__(self, strval):
        self.strval = strval

    def str_w(self, space):
        return self.strval