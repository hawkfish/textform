from .common import TransformException
from .transform import Transform

class Drop(Transform):
    def __init__(self, source, inputs):
        super().__init__('drop', inputs, (), source)

        if not source:
            raise TransformException(f"Can't Drop from missing input.")

        schema = source.schema()
        for input in self._inputs:
            if input not in schema:
                raise TransformException(f"Missing field '{input}' in Drop.")

    def _delete_inputs(self, d):
        for input in self._inputs:
            del d[input]
        return d

    def schema(self):
        return self._delete_inputs(super().schema())

    def next(self):
        return self._delete_inputs(super().next())
