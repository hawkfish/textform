from .common import TransformException
from .layouts import DictReaderFactory
from .transform import Transform

import csv

class Read(Transform):
    def __init__(self, iterable, source=None, layout='csv', **config):
        name = 'read'
        self._reader = DictReaderFactory(name, layout, iterable, None, **config)

        super().__init__(name, (), self._reader.fieldnames, source)

        self._validateOutputs()

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            Transform._addSchemaType(schema, output)
        return schema

    def readrow(self):
        row = super().readrow()
        r = next(self._reader)
        row.update(r)
        self._updateSchemaTypes(row, self.outputs)
        return row
