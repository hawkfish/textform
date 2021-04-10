from .common import TransformException
from .format import Format

def bind_fill(default):

    filler = default

    def fill(value):
        if isinstance(value, dict): return value

        nonlocal filler

        result = value
        if value:
            filler = result
        else:
            result = filler

        return result

    return fill

class Fill(Format):
    def __init__(self, source, input, default=''):
        super().__init__(source, input, bind_fill(default))

        self.name = 'fill'
        self.default = default
