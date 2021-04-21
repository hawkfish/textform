from .merge import Merge
from .transform import Transform
from .common import TransformException
from .layouts import WriterIterator, WriterFactory

def bind_nest(name, layout, inputs, **config):

    queue = WriterIterator()
    writer = WriterFactory(name, layout, queue, inputs, **config)

    def nest(values):
        nonlocal inputs, queue, writer
        writer.writerow(values)

        return next(queue)

    return nest

class Nest(Merge):
    def __init__(self, source, inputs, output, layout='csv', **config):
        name = 'nest'
        inputs = Transform._validateStringTuple(name, inputs, 'Input')

        super().__init__(source, inputs, output, bind_nest(name, layout, inputs, **config))

        self.name = name
        self.layout = layout
