from minijs import consts
from minijs.astcompiler import CompilerContext
from minijs.objects.floatobject import W_FloatObject
from minijs.parser import Transformer, _parse


class ObjectSpace(object):
    def parse(self, source):
        return Transformer().visit_main(_parse(source))

    def compile(self, source):
        astnode = self.parse(source)
        c = CompilerContext(self)
        astnode.compile(c)
        c.emit(consts.RETURN_NULL)
        return c.create_bytecode()


    def newfloat(self, floatval):
        return W_FloatObject(floatval)