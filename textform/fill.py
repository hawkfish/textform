from .common import TransformException
from .transform import Transform

class Fill(Transform):
    def __init__(self, source, input, default=''):
        super().__init__('fill', (input,), (), source)

        self._default = default
        self._fill = default

    def input(self): return self._inputs[0]
    def default(self): return self._default

    def next(self):
        row = super().next()
        if row is not None:
            value = row[self.input()]
            if value:
                self._fill = value
            else:
                row[self.input()] = self._fill

        return row
