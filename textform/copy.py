from .common import TransformException
from .transform import Transform

class Copy(Transform):
    def __init__(self, source, input, outputs):
        super().__init__('copy', (input,), outputs, source)

        self._requireSource()
        self._validateOutputs()

    def _fan_out(self, d):
        if d is not None:
            for output in self.outputs:
                d[output] = d[self.input]
        return d

    def _layout(self):
        #   Copy doesn't drop the inputs
        layout = self.source._layout()
        #   Output is inserted after the last input
        rightmost = layout.index(self.input) + 1
        layout[rightmost:rightmost] = list(self.outputs)

        return layout

    def _schema(self):
        return self._fan_out(super()._schema())

    def next(self):
        return self._fan_out(super().next())
