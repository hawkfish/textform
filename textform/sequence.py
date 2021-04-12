from .common import TransformException
from .transform import Transform

class Sequence(Transform):
    def __init__(self, source, output, start=0, step=1):
        self.start = start
        self.step = step

        super().__init__('sequence', (), (output,), source)

        self._validateOutputs();

        self._position = self.start

    def _schema(self):
        schema = super()._schema()
        Transform._addSchemaType(schema, self.output, type(self.start))
        return schema

    def next(self):
        row = super().next()
        row[self.output] = self._position
        self._position += self.step
        return row
