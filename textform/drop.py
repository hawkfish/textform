from .common import TransformException
from .transform import Transform

class Drop(Transform):
    def __init__(self, source, inputs):
        super().__init__('drop', inputs, (), source)

    def _delete_inputs(self, d):
        for input in self.inputs:
            del d[input]
        return d

    def layout(self):
        layout = self.source.layout() if self.source else []
        layout = list(filter(lambda input: input not in self.inputs, layout))
        return layout

    def schema(self):
        return self._delete_inputs(super().schema())

    def next(self):
        return self._delete_inputs(super().next())
