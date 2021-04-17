from .split import Split
from .transform import Transform
from .common import TransformException
from .formats import ReaderFactory, ReaderIterator

def bind_unnest(name, format, outputs, **config):

    queue = ReaderIterator()
    reader = ReaderFactory(name, format, queue, **config)

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
    def __init__(self, source, input, outputs, format='csv', **config):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(name, format, outputs, **config))

        self.name = name
