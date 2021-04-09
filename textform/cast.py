from .common import TransformException
from .transform import Transform

class Cast(Transform):
    def __init__(self, source, input, result_type):
        self.result_type = result_type

        super().__init__('cast', (input,), (), source)

    def _schema(self):
        schema = super()._schema()
        schema[self.input]['type'] = self.result_type
        return schema

    def next(self):
        row = super().next()
        if row is not None:
            row[self.input] = self.result_type(row[self.input])
        return row
