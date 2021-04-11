from .common import TransformException, MakeLineReader
from .transform import Transform

import csv

class Read(Transform):
    def __init__(self, iterable, source=None, format='csv', **config):
        name = 'read'
        self._reader = MakeLineReader(name, format, iterable, **config)

        super().__init__(name, (), self._reader.fieldnames, source)

        self._requireOutputs()
        self._typed = False

    def _schema(self):
        schema = super()._schema()
        schema.update({output: {'type': None} for output in self.outputs})
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            try:
                row.update(next(self._reader))
                if not self._typed:
                    for output in self.outputs:
                        self.schema[output] = {'type': type(row[output])}
                    self._typed = True

            except StopIteration:
                row = None

        return row
