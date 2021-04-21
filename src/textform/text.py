from .read import Read

class Text(Read):
    def __init__(self, iterable, output, source=None):
        config = {'default_fieldnames': (output,)}
        super().__init__(iterable, source, layout='text', **config)

        self.name = 'text'

        #   We know the output is text
        self.updateSchemaType(output, str)
