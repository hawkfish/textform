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
        super().__init__(source, input, bind_fill(default, blank))

        self.name = 'fill'
        self.default = default

        #   The type doesn't change
        self.schema[self.input] = copy.copy(self.source.schema[self.input])
        self._typed = True

FillDown = Fill
