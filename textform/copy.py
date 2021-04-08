from .common import TransformException
from .transform import Transform

class Copy(Transform):
    def __init__(self, source, input, outputs):
        super().__init__('copy', (input,), outputs, source)

        self._requireSource()
        self._requireOutputs()

    def input(self):
        return self._inputs[0]

    def _fan_out(self, d):
        if d is not None:
            for output in self._outputs:
                d[output] = d[self.input()]
        return d

    def layout(self):
        #   Copy doesn't drop the inputs
        layout = self._source.layout() if self._source else []
        #   Outputs are inserted at the first removed input
        rightmost = layout.index(self.input()) + 1
        layout[rightmost:] = list(self.outputs())

        return layout

    def schema(self):
        return self._fan_out(super().schema())

    def next(self):
        return self._fan_out(super().next())
