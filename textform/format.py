from .common import TransformException
from .transform import Transform

import re

class Format(Transform):
    def __init__(self, source, input, pattern, replace):
        super().__init__('format', (input,), (), source)

        self.search = re.compile(pattern)
        self.replace = replace

    def next(self):
        row = super().next()
        if row is not None:
            match = self.search.search(row[self.input])
            if match:
                row[self.input] = match.expand(self.replace)
        return row
