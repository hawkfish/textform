from .common import TransformException
from .transform import Transform

import re

class Format(Transform):
    def __init__(self, source, input, search, replace):
        super().__init__('format', (input,), (), source)

        self.input = self._inputs[0]
        self.search = re.compile(search)
        self.replace = replace

    def next(self):
        row = super().next()
        if row is not None:
            match = self.search.search(row[self.input])
            if match:
                row[self.input] = match.expand(self.replace)
        return row
