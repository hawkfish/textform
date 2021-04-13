from .merge import Merge
from .transform import Transform
from .common import TransformException, MakeFieldWriter

#   deque doesn't like to be modified while iterating
class WriteAdapter(object):

    def __init__(self):
        self.buffer = None
        self.buffered = False

    def __iter__(self):
        return self

    def write(self, value):
        if not self.buffered:
            self.buffer = value
            self.buffered = True
        else:
            self.buffer += value

    def __next__(self):
        if not self.buffered: raise StopIteration("Unnest NextAdapter")

        result = self.buffer
        self.buffered = False

        return result[:-1] if isinstance(result, str) else result

    next = __next__

def bind_nest(name, format, inputs, **config):

    if format == 'jsonl': format = 'json'

    queue = WriteAdapter()
    writer = MakeFieldWriter(name, format, queue, inputs, **config)

    def unnest(value):
        nonlocal inputs, queue, writer

        writer.writerow({input: value[i] for i, input in enumerate(inputs)})

        return next(queue)

    return unnest

class Nest(Merge):
    def __init__(self, source, inputs, output, format='csv', **config):
        name = 'nest'
        inputs = Transform._validateStringTuple(name, inputs, 'Input')

        super().__init__(source, inputs, output, bind_nest(name, format, inputs, **config))

        self.name = name
        self.format = format
