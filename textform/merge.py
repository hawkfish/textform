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

        self._typed = False

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
            value = self.merger([row[input] for input in self.inputs])
            for input in self.inputs:
                del row[input]
            row[self.output] = value
            if not self._typed:
                self.schema[self.output] = {'type': type(value)}
                self._typed = True

        return row
