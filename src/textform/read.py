from .common import TransformException, MakeLineReader
from .transform import Transform

import csv

class Read(Transform):
    def __init__(self, iterable, source=None, format='csv', **config):
        name = 'read'
        self._reader = MakeLineReader(name, format, iterable, None, **config)

        super().__init__(name, (), self._reader.fieldnames, source)

        self._validateOutputs()

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            Transform._addSchemaType(schema, output)
        return schema

    def readrow(self):
        row = super().readrow()
        row.update(next(self._reader))
        self._updateSchemaTypes(row, self.outputs)
        return row
