from .common import TransformException
from .transform import Transform

class Cast(Transform):
    def __init__(self, source, input, type_):
        super().__init__('cast', (input,), (), source)

        self._type = type_

        self._requireSource()

    def input(self): return self._inputs[0]
    def type(self): return self._type

    def schema(self):
        schema = super().schema()
        schema[self.input()]['type'] = self._type
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            row[self.input()] = self._type(row[self.input()])
        return row
