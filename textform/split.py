from .common import TransformException
from .transform import Transform

import copy

def bind_split(separator, outputs, defaults):

    if callable(separator):
        return separator

    def split(value):
        nonlocal separator, outputs, defaults

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

        self._validateOutputs(self.inputs)

        #   Dynamic typing
        self._typed = False

    def _schema(self):
        schema = super()._schema()
        del schema[self.input]
        schema.update({output: {'type': None} for output in self.outputs})
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            updates = self.function(row[self.input])
            del row[self.input]
            row.update(updates)
            if not self._typed:
                self.schema.update({k: {'type': type(updates[k])} for k in updates})
                self._typed = True

        return row
