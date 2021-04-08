from .common import TransformException
from .transform import Transform

import copy

class Split(Transform):
    def __init__(self, source, input, outputs, sep, defaults=''):
        super().__init__('split', (input,), outputs, source)

        self._requireSource()
        self._requireOutputs(self._inputs)

        self._sep = sep

        if isinstance(defaults, (list, tuple,)):
            self._defaults = tuple(defaults)
        else:
            self._defaults = tuple([defaults for output in self._outputs])

        for default in self._defaults:
            if type(default) != str:
                raise TransformException(f"Default value '{default}' in {self.name()} is not a string")

        if len(self._defaults) != len(self._outputs):
            raise TransformException(f"Default count {len(self._defaults)} doesn't match the output count "
            f"{len(self._outputs)} in {self.name()}")

    def input(self): return self._inputs[0]
    def separator(self): return self._sep
    def defaults(self): return self._defaults

    def schema(self):
        schema = super().schema()
        value = schema[self.input()]
        del schema[self.input()]
        for output in self.outputs():
            schema[output] = copy.copy(value)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            parts = row[self.input()].split(self._sep, len(self._outputs))
            del row[self.input()]

            for i, part in enumerate(parts):
                row[self._outputs[i]] = part

            for i in range(len(parts), len(self._outputs)):
                row[self._outputs[i]] = self._defaults[i]

        return row
