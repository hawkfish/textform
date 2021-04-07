from .common import TransformException
from .transform import Transform

class Copy(Transform):
    def __init__(self, source, input, outputs):
        super().__init__('copy', input, outputs, source)

        if len(self._inputs) != 1:
            raise TransformException(f"Wrong number of inputs to Copy {len(self._inputs)}.")

        if not source:
            raise TransformException(f"Can't Copy from missing input.")

        schema = source.schema()
        if self.input() not in schema:
            raise TransformException(f"Copy input field '{self.input()}' missing.")

        for output in self._outputs:
            if output in schema:
                raise TransformException(f"Copy output field '{output}' overwrites an existing field.")

    def input(self):
        return self._inputs[0]

    def _fan_out(self, d):
        if d is not None:
            for idx, output in enumerate(self._outputs):
                d[output] = d[self.input()]
        return d

    def schema(self):
        return self._fan_out(super().schema())

    def next(self):
        return self._fan_out(super().next())
