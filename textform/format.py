from .common import TransformException
from .transform import Transform

import re

class Format(Transform):
    def __init__(self, source, input, function):
        self.function = function

        super().__init__('format', (input,), (), source)

    def _schema(self):
        schema = super()._schema()
        schema[self.input] = self.function(schema[self.input])
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            row[self.input] = self.function(row[self.input])
        return row
