from .split import Split
from .transform import Transform
from .common import TransformException
from .layouts import LineReaderFactory, BufferedAppender

def bind_unnest(name, layout, outputs, **config):

    queue = BufferedAppender()
    reader = LineReaderFactory(name, layout, queue, **config)

    def unnest(value):
        nonlocal queue, reader, outputs

        queue.append(value)

        result = next(reader)

        if isinstance(result, dict):
            result = [result[output] for output in outputs]

        elif not isinstance(result, (list, tuple,)):
            result = [result,]

        return result

    return unnest

class Unnest(Split):
    def __init__(self, source, input, outputs, layout='csv', **config):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(name, layout, outputs, **config))

        self.name = name
