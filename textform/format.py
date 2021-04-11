from .common import TransformException
from .transform import Transform

import re

class Format(Transform):
    def __init__(self, source, input, function):
        self.function = function

        super().__init__('format', (input,), (), source)

        self._typed = False

    def _schema(self):
        schema = super()._schema()
        schema[self.input] = {'type': None}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            row[self.input] = self.function(row[self.input])
            if not self._typed:
                self.schema[self.input] = {'type': type(row[self.input])}
                self._typed = True
        return row
