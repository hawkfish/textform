from .common import TransformException
from .read import Read

class Text(Read):
    def __init__(self, iterable, output, source=None):
        params = {'format': 'text', 'fieldnames': (output,)}
        super().__init__(iterable, source, **params)

        self.name = 'text'
