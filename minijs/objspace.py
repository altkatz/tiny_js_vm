from minijs.parser import Transformer, _parse


class ObjectSpace(object):
    def parse(self, source):
        return Transformer().visit_main(_parse(source))