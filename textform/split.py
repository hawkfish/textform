from .common import TransformException
from .transform import Transform

import copy

def bind_split(separator, outputs, defaults):

    if not isinstance(separator, str):
        return separator

    def split(value):
        nonlocal separator, outputs, defaults

        if isinstance(value, dict):
            return {outputs[i]: copy.copy(value) for i in range(len(outputs))}

        parts = value.split(separator, len(defaults))
        while len(parts) < len(defaults):
            parts.append(defaults[len(parts)])

        return {outputs[i]: parts[i] for i in range(len(outputs))}

    return split

class Split(Transform):
    def __init__(self, source, input, outputs, separator, defaults=''):
        name = 'split'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        self.function = bind_split(separator, outputs, defaults)

        super().__init__('split', (input,), outputs, source)

        self.separator = separator
        self.defaults = defaults

        self._requireOutputs(self.inputs)

    def _schema(self):
        schema = super()._schema()
        updates = self.function(schema[self.input])
        del schema[self.input]
        schema.update(updates)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            updates = self.function(row[self.input])
            del row[self.input]
            row.update(updates)

        return row
