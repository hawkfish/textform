from .common import TransformException
from .transform import Transform

import re

def bind_divide(pattern):

    if callable(pattern):
        return pattern

    regexp = re.compile(pattern)

    def divide(value):
        nonlocal regexp

        return True if regexp.search(value) else False

    return divide

class Divide(Transform):
    def __init__(self, source, input, passed, failed, pattern, fills=''):
        super().__init__('divide', (input,), (passed, failed,), source)

        self._validateOutputs(self.inputs)

        self.passed = self.outputs[0]
        self.failed = self.outputs[1]
        self.pattern = pattern
        self.fills = Transform._validateTupleParameter(self.name, fills, 'Fill', 2)

        self.predicate = bind_divide(self.pattern)

    def _schema(self):
        schema = super()._schema()
        metadata = schema[self.input]
        del schema[self.input]
        schema.update({output: metadata for output in self.outputs})
        return schema

    def readrow(self):
        row = super().readrow()
        value = row[self.input]
        del row[self.input]

        if self.predicate(value):
            row[self.passed] = value
            row[self.failed] = self.fills[1]
        else:
            row[self.passed] = self.fills[0]
            row[self.failed] = value

        self._updateSchemaTypes(row, self.outputs)

        return row
