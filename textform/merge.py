from .common import TransformException
from .transform import Transform

class Merge(Transform):
    def __init__(self, source, inputs, output, glue=''):
        super().__init__('merge', inputs, (output,), source)

        self._requireSource()
        self._requireOutputs(self._inputs)

        self._glue = glue

    def output(self): return self._outputs[0]
    def glue(self): return self._glue

    def schema(self):
        schema = super().schema()
        metadata = {}
        for input in self._inputs:
            metadata = schema[input]
            del schema[input]
        schema[self.output()] = metadata
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            value = self._glue.join([row[input] for input in self._inputs])
            for input in self._inputs:
                del row[input]
            row[self.output()] = value

        return row
