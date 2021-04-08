from .common import TransformException
from .transform import Transform

import re

class Match(Transform):
    def __init__(self, source, input, pattern, invert=False):
        super().__init__('match', (input,), (), source)

        self._requireSource()

        self._regexp = re.compile(pattern)
        self._invert = True if invert else False

    def input(self): return self._inputs[0]
    def regexp(self): return self._regexp
    def invert(self): return self._invert

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            matched = self._regexp.search(row[self.input()])
            if (matched and not self.invert()) or (self.invert() and not matched):
                return row

        return None
