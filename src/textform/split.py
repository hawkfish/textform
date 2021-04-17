from .common import TransformException
from .transform import Transform

import copy

def bind_split(separator, outputs):

    if callable(separator):
        return separator

    def split(value):
        nonlocal separator, outputs

        return value.split(separator, len(outputs))

    return split

class Split(Transform):
    def __init__(self, source, input, outputs, separator, defaults=''):
        name = 'split'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        self.function = bind_split(separator, outputs)

        super().__init__('split', (input,), outputs, source)

        self.separator = separator
        self.defaults = defaults

        self._validateOutputs(self.inputs)

    def _schema(self):
        schema = super()._schema()
        shared = schema[self.input]
        del schema[self.input]
        for output in self.outputs:
            Transform._addSchemaType(schema, output)
        return schema

    def readrow(self):
        row = super().readrow()
        parts = list(self.function(row[self.input]))
        del row[self.input]

        while len(parts) < len(self.defaults):
            parts.append(self.defaults[len(parts)])

        row.update(dict(zip(self.outputs, parts)))
        self._updateSchemaTypes(row, self.outputs)

        return row
