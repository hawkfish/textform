from .common import TransformException
from .transform import Transform

import copy

def bind_split(separator, defaults):

    if not isinstance(separator, str):
        return separator

    def split(arg):
        nonlocal separator, defaults

        if isinstance(arg, dict):
            return [copy.copy(arg) for default in defaults]

        parts = arg.split(separator, len(defaults))
        while len(parts) < len(defaults):
            parts.append(defaults[len(parts)])

        return parts

    return split

class Split(Transform):
    def __init__(self, source, input, outputs, separator, defaults=''):
        name = 'split'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        self.function = bind_split(separator, defaults)

        super().__init__('split', (input,), outputs, source)

        self.separator = separator
        self.defaults = defaults

        self._requireOutputs(self.inputs)

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
            parts = self.function(row[self.input])
            del row[self.input]

            for i, part in enumerate(parts):
                row[self.outputs[i]] = part

        return row
