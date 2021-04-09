from .common import TransformException
from .transform import Transform

class Merge(Transform):
    def __init__(self, source, inputs, output, glue=''):
        super().__init__('merge', inputs, (output,), source)

        self.glue = glue

        self._requireOutputs(self.inputs)

    def _schema(self):
        schema = super()._schema()
        metadata = {}
        for input in self.inputs:
            metadata = schema[input]
            del schema[input]
        schema[self.output] = metadata
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            value = self.glue.join([row[input] for input in self.inputs])
            for input in self.inputs:
                del row[input]
            row[self.output] = value

        return row
