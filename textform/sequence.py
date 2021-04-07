from .common import TransformException
from .transform import Transform

class Sequence(Transform):
    def __init__(self, source, output, start=0, step=1):
        super().__init__('sequence', (), output, source)

        if len(self._outputs) != 1:
            raise TransformException(f"Wrong number of inputs to {self._name}: {len(self._inputs)}.")

        if self.output() in super().schema():
            raise TransformException(f"Output field '{output}' in {self._name} overwrites an existing field.")

        self._start = start
        self._step = step

        self._position = self._start

    def output(self): return self._outputs[0]
    def start(self): return self._start
    def step(self): return self._step
    def position(self): return self._position

    def schema(self):
        schema = super().schema()
        schema[self.output()] = {'type': int}
        return schema

    def next(self):
        row = super().next()
        row[self.output()] = self._position
        self._position += self._step
        return row
