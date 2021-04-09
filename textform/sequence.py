from .common import TransformException
from .transform import Transform

class Sequence(Transform):
    def __init__(self, source, output, start=0, step=1):
        super().__init__('sequence', (), (output,), source)

        self._requireOutputs();

        self.start = start
        self.step = step

        self._position = self.start

    def _schema(self):
        schema = super()._schema()
        schema[self.output] = {'type': int}
        return schema

    def next(self):
        row = super().next()
        row[self.output] = self._position
        self._position += self.step
        return row
