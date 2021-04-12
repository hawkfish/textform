from .common import TransformException
from .transform import Transform

def bind_merge(glue):

    if callable(glue):
        return glue

    def merge(values):
        nonlocal glue

        return glue.join(values)

    return merge

class Merge(Transform):
    def __init__(self, source, inputs, output, glue=''):
        super().__init__('merge', inputs, (output,), source)

        self.glue = glue
        self.merger = bind_merge(glue)

        self._validateOutputs(self.inputs)

    def _schema(self):
        schema = super()._schema()
        dtype = None
        for input in self.inputs:
            dtype = Transform._getSchemaType(schema, input)
            del schema[input]
        Transform._addSchemaType(schema, self.output)
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            value = self.merger([row[input] for input in self.inputs])
            for input in self.inputs:
                del row[input]
            row[self.output] = value

            self._updateSchemaTypes(row, self.outputs)

        return row
