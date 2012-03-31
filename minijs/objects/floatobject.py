from minijs.objects.base import W_Root


class W_FloatObject(W_Root):
    def __init__(self, floatval):
        self.floatval = floatval

    def float_w(self, space):
        return self.floatval

    def str(self, space):
        return space.newstr(str(self.floatval))

    def sub(self, space, w_other):
        return space.newfloat(self.floatval - space.float_w(w_other))
    def ge(self, space, w_other):
        floatval = space.float_w(w_other)
        return space.newbool(self.floatval >= floatval)