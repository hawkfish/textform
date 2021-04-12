from .read import Read

class Text(Read):
    def __init__(self, iterable, output, source=None):
        config = {'fieldnames': (output,)}
        super().__init__(iterable, source, format='text', **config)

        self.name = 'text'
