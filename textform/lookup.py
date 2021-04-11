from .common import TransformException
from .format import Format

def bind_lookup(table, default):

    for key in table:
        if type(table[key]) != type(default):
            raise TransformException(f"Type mismatch in {name} between the table and the default")

    def lookup(value):
        nonlocal table, default
        if isinstance(value, dict): return {'type': type(default)}

        return table.get(value, default)

    return lookup

class Lookup(Format):
    def __init__(self, source, input, table, default):
        super().__init__(source, input, bind_lookup(table, default))

        self.name = 'lookup'
        self.table = table
        self.default = default
