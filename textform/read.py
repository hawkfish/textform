from .common import TransformException, MakeLineReader
from .transform import Transform

import csv

class Read(Transform):
    def __init__(self, iterable, source=None, format='csv', **config):
        name = 'read'
        self._reader = MakeLineReader(name, format, iterable, **config)

        super().__init__(name, (), self._reader.fieldnames, source)

        self._validateOutputs()

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            Transform._addSchemaType(schema, output)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            try:
                row.update(next(self._reader))
                if not self._typed:
                    self._updateSchemaTypes(row, self.outputs)

            except StopIteration:
                row = None

        return row
