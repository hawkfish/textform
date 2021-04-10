from .common import TransformException
from .format import Format

def bind_fill(default, blank):

    filler = default

    def fill(value):
        if isinstance(value, dict): return value

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

FillDown = Fill
