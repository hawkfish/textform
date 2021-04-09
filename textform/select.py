from .common import TransformException
from .transform import Transform

import re

class Select(Transform):
    def __init__(self, source, inputs, predicate):
        super().__init__('select', inputs, (), source)

        self._requireSource()

        self.predicate = predicate

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            #   Bind the input values
            args = tuple([row[input] for input in self.inputs])
            if self.predicate(*args):
                return row

        return None
