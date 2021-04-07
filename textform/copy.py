from .common import TransformException
from .transform import Transform

class Copy(Transform):
    def __init__(self, source, input, outputs):
        super().__init__('copy', (input,), outputs, source)

        if not source:
            raise TransformException(f"Can't {self._name} from missing input.")

        schema = source.schema()
        if self.input() not in schema:
            raise TransformException(f"Missing input field '{self.input()}' in {self._name}.")

        for output in self._outputs:
            if output in schema:
                raise TransformException(f"Output field '{output}' in {self._name} overwrites an existing field.")

    def input(self):
        return self._inputs[0]

    def _fan_out(self, d):
        if d is not None:
            for output in self._outputs:
                d[output] = d[self.input()]
        return d

    def schema(self):
        return self._fan_out(super().schema())

    def next(self):
        return self._fan_out(super().next())
