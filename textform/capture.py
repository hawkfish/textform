from .common import TransformException
from .transform import Transform

import copy
import re

class Capture(Transform):
    def __init__(self, source, input, outputs, pattern):
        super().__init__('capture', (input,), outputs, source)

        self._requireSource()
        self._requireOutputs(self._inputs)

        self._regexp = re.compile(pattern)
        if self._regexp.groups != len(self._outputs):
            raise TransformException(f"Group count {self._regexp.groups} doesn't match the output count "
            f"{len(self._outputs)} in {self.name()}")

    def input(self): return self._inputs[0]
    def regexp(self): return self._regexp

    def schema(self):
        schema = super().schema()
        value = schema[self.input()]
        del schema[self.input()]
        for output in self._outputs:
            schema[output] = copy.copy(value)
        return schema

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            value = row[self.input()]
            del row[self.input()]

            match = self._regexp.search(value)
            if match:
                for i, output in enumerate(self._outputs):
                    row[output] = match.group(i+1)
                return row

        return None
