from .common import TransformException
from .transform import Transform

import copy

class Split(Transform):
    def __init__(self, source, input, outputs, sep, defaults=''):
        super().__init__('split', (input,), outputs, source)

        self._requireSource()
        self._requireOutputs(self.inputs)

        self.separator = sep

        if isinstance(defaults, (list, tuple,)):
            self.defaults = tuple(defaults)
        else:
            self.defaults = tuple([defaults for output in self.outputs])

        for default in self.defaults:
            if type(default) != str:
                raise TransformException(f"Default value '{default}' in {self.name} is not a string")

        if len(self.defaults) != len(self.outputs):
            raise TransformException(f"Default count {len(self.defaults)} doesn't match the output count "
            f"{len(self.outputs)} in {self.name}")

    def schema(self):
        schema = super().schema()
        value = schema[self.input]
        del schema[self.input]
        for output in self.outputs:
            schema[output] = copy.copy(value)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            parts = row[self.input].split(self.separator, len(self.outputs))
            del row[self.input]

            for i, part in enumerate(parts):
                row[self.outputs[i]] = part

            for i in range(len(parts), len(self.outputs)):
                row[self.outputs[i]] = self.defaults[i]

        return row
