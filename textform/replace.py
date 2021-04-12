from .common import TransformException
from .format import Format
from .transform import Transform

import copy
import re

def bind_replace(pattern, expansion):

    search = re.compile(pattern)

    def replace(arg):
        match = search.search(arg)
        if match:
            return match.expand(expansion)
        else:
            return arg

    return replace

class Replace(Format):
    def __init__(self, source, input, pattern, replace):
        super().__init__(source, input, bind_replace(pattern, replace))

        self.name = 'replace'
        self.search = re.compile(pattern)
        self.replace = replace

    def _schema(self):
        schema = super()._schema()
        #   The result type is string
        Transform._updateSchemaType(schema, self.input, str)
        return schema
