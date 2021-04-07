from .common import TransformException
from .transform import Transform

class Add(Transform):
    def __init__(self, source, outputs, values):
        super().__init__('add', (), outputs, source)

        self._values = values
        if isinstance(self._values, (tuple, list)):
            self._values = tuple(self._values)
        else:
            self._values = (self._values,)

        if source:
            schema = source.schema()
            for output in self._outputs:
                if output in schema:
                    raise TransformException(f"Add output field '{output}' overwrites an existing field.")

        if len(self._values) != len(self._outputs):
            raise TransformException(f"Added value count {len(self._values)} doesn't match the output count "
            f"{len(self._outputs)}")

    def values(self): return self._values

    def schema(self):
        schema = super().schema()
        for idx, output in enumerate(self._outputs):
            schema[output] = {'type': type(self._values[idx])}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            for idx, output in enumerate(self._outputs):
                row[output] = self._values[idx]
        return row
