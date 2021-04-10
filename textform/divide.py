from .common import TransformException
from .transform import Transform

import copy
import re

def bind_divide(name, pattern, fills):

    regexp = re.compile(pattern)

    def divide(value):
        nonlocal regexp, fills

        if isinstance(value, dict): return [copy.copy(value) for i in range(2)]

        if regexp.search(value):
            return (value, fills[1],)
        else:
            return (fills[0], value,)

    return divide

class Divide(Transform):
    def __init__(self, source, input, passed, failed, pattern, fills=''):
        name = 'divide'
        fills = Transform._validateStringTuple(name, fills, 'Fill', 2)
        self.function = bind_divide(name, pattern, fills)

        super().__init__(name, (input,), (passed, failed,), source)

        self._requireOutputs(self.inputs)

        self.passed = self.outputs[0]
        self.failed = self.outputs[1]
        self.pattern = pattern
        self.fills = fills

    def _schema(self):
        schema = super()._schema()
        metadata = self.function(schema[self.input])
        del schema[self.input]
        for i, output in enumerate(self.outputs):
            schema[output] = metadata[i]
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            values = self.function(row[self.input])
            del row[self.input]

            for i, output in enumerate(self.outputs):
                row[output] = values[i]

        return row
