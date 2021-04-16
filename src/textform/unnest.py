from .split import Split
from .transform import Transform
from .common import TransformException
from .formats import ReaderFactory, ReaderIterator

def bind_unnest(name, format, outputs, **config):

    queue = ReaderIterator()
    reader = ReaderFactory(name, format, queue, **config)

    def unnest(value):
        nonlocal queue, reader, outputs

        if value is None: raise Exception
        queue.append(value)

        result = {output: None for output in outputs}

        values = next(reader)
        if isinstance(values, dict):
            result.update(values)

        elif isinstance(values, (list, tuple,)):
            result.update(dict(zip(outputs, values)))

        else:
            result = {output: values for output in outputs}

        return result

    return unnest

class Unnest(Split):
    def __init__(self, source, input, outputs, format='csv', **config):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(name, format, outputs, **config))

        self.name = name
