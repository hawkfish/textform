from .common import TransformException
from .format import Format
from .transform import Transform

def bind_lookup(table, default):

    def lookup(value):
        nonlocal table, default

        return table.get(value, default)

    return lookup

class Lookup(Format):
    def __init__(self, source, input, table, default):

        name = 'lookup'
        for key in table:
            if type(table[key]) != type(default):
                raise TransformException(f"Type mismatch in {name} between the table and the default")

        self.table = table
        self.default = default

        super().__init__(source, input, bind_lookup(table, default))

        self.name = 'lookup'

    def _schema(self):
        schema = super()._schema()
        #   The type is known from the default
        Transform._addSchemaType(schema, self.input, type(self.default))
        return schema
