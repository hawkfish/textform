from .common import TransformException
from .transform import Transform

class Text(Transform):
    def __init__(self, text, output, source=None):
        super().__init__('text', (), (output,), source)

        self._requireOutputs()

        self._text = text

    def _schema(self):
        schema = super()._schema()
        schema[self.output] = {'type': str}
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            line = self._text.readline()
            if line:
                #   Only remove the newline - blanks may be important
                row[self.output] = line[:-1] if line[-1] == '\n' else line
            else:
                row = None

        return row
