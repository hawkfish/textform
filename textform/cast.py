from .format import Format
from .transform import Transform

class Cast(Format):
    def __init__(self, source, input, result_type):
        self.result_type = result_type

        super().__init__(source, input, result_type)

        self.name = 'cast'

    def _schema(self):
        schema = super()._schema()
        #   We know the result type, and it replaces the old one
        Transform._addSchemaType(schema, self.input, self.result_type)
        return schema
