from .common import TransformException
from .split import Split
from .transform import Transform

import copy
import csv

#   deque doesn't like to be modified while iterating
class NextAdapter(object):

    def __init__(self):
        self.buffered = None

    def __iter__(self):
        return self

    def append(self, value):
        self.buffered = str(value)

    def __next__(self):
        result = self.buffered
        self.buffered = None
        return result

    next = __next__

def bind_unnest(outputs):

    queue = NextAdapter()
    reader = csv.DictReader(queue, outputs)

    def unnest(value):
        nonlocal queue, reader, outputs

        if isinstance(value, dict):
            return {output: copy.copy(value) for output in outputs}

        queue.append(value)

        return next(reader)

    return unnest

class Unnest(Split):
    def __init__(self, source, input, outputs):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(outputs))

        self.name = name
