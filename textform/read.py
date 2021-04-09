from .common import TransformException
from .transform import Transform

import csv

class Read(Transform):
    def __init__(self, stream, source=None):
        self._reader = csv.DictReader(stream)

        super().__init__('read', (), self._reader.fieldnames, source)

        self._requireOutputs()

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            schema[output] = {'type': str}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            line = next(self._reader, None)
            if line:
                row.update(line)
            else:
                row = None

        return row
