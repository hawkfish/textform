from .split import Split
from .transform import Transform
from .common import TransformException
from .formats import UnnesterFactory

#   deque doesn't like to be modified while iterating
class NextAdapter(object):

    def __init__(self):
        self.buffer = None
        self.buffered = False

    def __iter__(self):
        return self

    def append(self, value):
        self.buffer = value
        self.buffered = True

    def __next__(self):
        if not self.buffered: raise StopIteration("Unnest NextAdapter")

        result = self.buffer
        self.buffered = False
        return result

    next = __next__

def bind_unnest(name, format, outputs, **config):

    queue = NextAdapter()
    reader = UnnesterFactory(name, format, queue, outputs, **config)

    def unnest(value):
        nonlocal queue, reader, outputs

        queue.append(value)

        return next(reader)

    return unnest

class Unnest(Split):
    def __init__(self, source, input, outputs, format='csv', **config):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(name, format, outputs, **config))

        self.name = name
