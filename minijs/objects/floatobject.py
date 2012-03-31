from minijs.objects.base import W_Root


class W_FloatObject(W_Root):
    def __init__(self, floatval):
        self.floatval = floatval

    def str(self, space):
        return space.newstr(str(self.floatval))