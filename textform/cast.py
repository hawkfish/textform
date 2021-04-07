from .common import TransformException
from .transform import Transform

class Cast(Transform):
    def __init__(self, source, input, type_):
        super().__init__('cast', (input,), (), source)

        if not source:
            raise TransformException(f"Can't Cast from missing input.")

        if len(self._inputs) != 1:
            raise TransformException(f"Wrong number of inputs to Cast {len(self._inputs)}.")

        schema = source.schema()
        if self.input() not in schema:
            raise TransformException(f"Cast input field '{self.input()}' missing.")

        self._type = type_

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
