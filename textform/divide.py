from .common import TransformException
from .transform import Transform

import copy
import re

class Divide(Transform):
    def __init__(self, source, input, passed, failed, pattern, fills=''):
        super().__init__('divide', (input,), (passed, failed,), source)

        if not source:
            raise TransformException(f"Can't {self._name} from missing input.")

        schema = source.schema()
        if self.input() not in schema:
            raise TransformException(f"Missing input field '{self.input()}' in {self._name}.")

        for output in self._outputs:
            if output in schema and output != input:
                raise TransformException(f"Output field '{output}' in {self._name} overwrites an existing field.")

        self._regexp = re.compile(pattern)

        if isinstance(fills, (list, tuple,)):
            self._fills = tuple(fills)
        else:
            self._fills = (fills, fills,)

        if len(self._fills) != len(self._outputs):
            raise TransformException(f"Fill count {len(self._fills)} doesn't match the output count "
            f"{len(self._outputs)} in {self.name()}")

    def input(self): return self._inputs[0]
    def passed(self): return self._outputs[0]
    def failed(self): return self._outputs[1]
    def regexp(self): return self._regexp
    def fills(self): return self._fills

    def schema(self):
        schema = super().schema()
        value = schema[self.input()]
        del schema[self.input()]
        schema[self.passed()] = value
        schema[self.failed()] = copy.copy(value)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            value = row[self.input()]
            del row[self.input()]
            if self._regexp.search(value):
                row[self.passed()] = value
                row[self.failed()] = self._fills[1]
            else:
                row[self.passed()] = self._fills[0]
                row[self.failed()] = value

        return row
