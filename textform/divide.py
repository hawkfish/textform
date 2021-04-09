from .common import TransformException
from .transform import Transform

import copy
import re

class Divide(Transform):
    def __init__(self, source, input, passed, failed, pattern, fills=''):
        super().__init__('divide', (input,), (passed, failed,), source)

        self._requireSource()
        self._requireOutputs(self.inputs)

        self.passed = self.outputs[0]
        self.failed = self.outputs[1]

        self.regexp = re.compile(pattern)

        if isinstance(fills, (list, tuple,)):
            self.fills = tuple(fills)
        else:
            self.fills = (fills, fills,)

        if len(self.fills) != len(self.outputs):
            raise TransformException(f"Fill count {len(self.fills)} doesn't match the output count "
            f"{len(self.outputs)} in {self.name}")

    def schema(self):
        schema = super().schema()
        value = schema[self.input]
        del schema[self.input]
        schema[self.passed] = value
        schema[self.failed] = copy.copy(value)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            value = row[self.input]
            del row[self.input]
            if self.regexp.search(value):
                row[self.passed] = value
                row[self.failed] = self.fills[1]
            else:
                row[self.passed] = self.fills[0]
                row[self.failed] = value

        return row
