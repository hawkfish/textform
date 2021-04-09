from .common import TransformException
from .transform import Transform

class Add(Transform):
    def __init__(self, source, outputs, values):
        super().__init__('add', (), outputs, source)

        self.values = values
        if isinstance(self.values, (tuple, list)):
            self.values = tuple(self.values)
        else:
            self.values = (self.values,)

        self._requireOutputs()

        if len(self.values) != len(self.outputs):
            raise TransformException(f"Added value count {len(self.values)} doesn't match the output count "
            f"{len(self.outputs)}")

    def schema(self):
        schema = super().schema()
        for idx, output in enumerate(self.outputs):
            schema[output] = {'type': type(self.values[idx])}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            for idx, output in enumerate(self.outputs):
                row[output] = self.values[idx]
        return row
