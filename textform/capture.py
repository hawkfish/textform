from .common import TransformException
from .transform import Transform

import copy
import re

class Capture(Transform):
    def __init__(self, source, input, outputs, pattern):
        super().__init__('capture', (input,), outputs, source)

        self._requireSource()
        self._requireOutputs(self.inputs)

        self.regexp = re.compile(pattern)
        if self.regexp.groups != len(self.outputs):
            raise TransformException(f"Group count {self.regexp.groups} doesn't match the output count "
            f"{len(self.outputs)} in {self.name}")

    def _schema(self):
        schema = super()._schema()
        value = schema[self.input]
        del schema[self.input]
        for output in self.outputs:
            schema[output] = copy.copy(value)
        return schema

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            value = row[self.input]
            del row[self.input]

            match = self.regexp.search(value)
            if match:
                for i, output in enumerate(self.outputs):
                    row[output] = match.group(i+1)
                return row

        return None
