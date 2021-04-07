from .common import TransformException
from .transform import Transform

import re

class Match(Transform):
    def __init__(self, source, input, pattern, invert=False):
        super().__init__('match', (input,), (), source)

        if not source:
            raise TransformException(f"Can't {self._name} from missing input.")

        if len(self._inputs) != 1:
            raise TransformException(f"Wrong number of inputs to {self._name}: {len(self._inputs)}.")

        schema = source.schema()
        if self.input() not in schema:
            raise TransformException(f"Missing input field '{self.input()}' in {self._name}.")

        self._regexp = re.compile(pattern)
        self._invert = True if invert else False

    def input(self): return self._inputs[0]
    def regexp(self): return self._regexp
    def invert(self): return self._invert

    def next(self):
        while True:
            row = super().next()
            if not row: break

            matched = self._regexp.search(row[self.input()])
            if (matched and not self.invert()) or (self.invert() and not matched):
                return row

        return None
