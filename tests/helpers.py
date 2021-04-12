from context import *

class MockEmpty(txf.Transform):
    def next(self) : return None

class MockSource(txf.Transform):
    def __init__(self, outputs):
        super().__init__('mock', (), outputs)

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            txf.Transform._addSchemaType(schema, output)
        return schema

    def next(self):
        return {output: None for output in self.outputs}

class MockAlternate(txf.Transform):
    def __init__(self, output, value, step=2, offset=0):
        self._value = str(value)

        super().__init__('mock', (), (output,), None)

        self._step = int(step)
        self._position = int(offset)

    def _schema(self):
        schema = super()._schema()
        txf.Transform._addSchemaType(schema, self.output, type(self._value))
        return schema

    def next(self):
        row = {self.output: self._value if 0 == (self._position % self._step) else ''}
        self._position += 1
        return row

