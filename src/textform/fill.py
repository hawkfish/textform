from .common import TransformException
from .format import Format

import copy

def bind_fill(default, blank):

    filler = default

    def fill(value):
        nonlocal filler, blank

        result = value
        if value == blank:
            result = filler
        else:
            filler = result

        return result

    return fill

class Fill(Format):
    def __init__(self, source, input, default='', blank=''):
        name = 'fill'
        if type(default) != type(blank):
            raise TransformException(f"Types of default and blank don't match in {name}")

        super().__init__(source, input, bind_fill(default, blank))

        self.name = name
        self.default = default

        #   The output is the same as the input
        self.schema[input] = source.schema[input]

FillDown = Fill
