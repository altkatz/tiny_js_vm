from minijs import consts
from minijs.astcompiler import CompilerContext
from minijs.interpreter import Interpreter, Frame
from minijs.objects.floatobject import W_FloatObject
from minijs.objects.stringobject import W_StringObject
from minijs.parser import Transformer, _parse


class ObjectSpace(object):
    def __init__(self, interpreter_cls=Interpreter):
        self.transformer = Transformer()
        self.interpreter = interpreter_cls()

    def parse(self, source):
        return self.transformer.visit_main(_parse(source))

    def compile(self, source):
        astnode = self.parse(source)
        c = CompilerContext(self)
        astnode.compile(c)
        c.emit(consts.RETURN_NULL)
        return c.create_bytecode()

    def exec_(self, source):
        bc = self.compile(source)
        self.interpreter.interpret(self, Frame(bc), bc)


    def newfloat(self, floatval):
        return W_FloatObject(floatval)

    def newstr(self, strval):
        return W_StringObject(strval)


    def str(self, w_obj):
        return w_obj.str(self)

    def str_w(self, w_obj):
        return w_obj.str_w(self)