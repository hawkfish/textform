from .common import TransformException
from .transform import Transform

class Drop(Transform):
    def __init__(self, source, inputs):
        super().__init__('drop', inputs, (), source)

    def _delete_inputs(self, d):
        for input in self._inputs:
            del d[input]
        return d

    def layout(self):
        layout = self._source.layout() if self._source else []
        layout = list(filter(lambda input: input not in self._inputs, layout))
        return layout

    def schema(self):
        return self._delete_inputs(super().schema())

    def next(self):
        return self._delete_inputs(super().next())
