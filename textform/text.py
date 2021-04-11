from .common import TransformException
from .transform import Transform

class Text(Transform):
    def __init__(self, text, output, source=None):
        super().__init__('text', (), (output,), source)

        self._requireOutputs()

        self._text = text
        self._typed = False

    def _schema(self):
        schema = super()._schema()
        schema[self.output] = {'type': None}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            try:
                line = next(self._text)
                if not self._typed:
                    self.schema[self.output] = {'type': type(line)}
                    self._typed = True

                row[self.output] = line

            except StopIteration:
                row = None

        return row
