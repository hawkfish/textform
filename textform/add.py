from .common import TransformException
from .transform import Transform

class Add(Transform):
    def __init__(self, source, outputs, values):
        self._setValues(values)

        super().__init__('add', (), outputs, source)

        self._validateOutputs()

    def _setValues(self, values):
        self.values = values

        if isinstance(self.values, (tuple, list)):
            self.values = tuple(self.values)
        else:
            self.values = (self.values,)

    def _schema(self):
        if len(self.values) != len(self.outputs):
            raise TransformException(f"Value count {len(self.values)} in {self.name} doesn't match the output count "
                                     f"{len(self.outputs)}")

        schema = super()._schema()
        for i, output in enumerate(self.outputs):
            Transform._addSchemaType(schema, output, type(self.values[i]))
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            row.update({output: self.values[i] for i, output in enumerate(self.outputs)})
        return row
