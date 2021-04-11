from .common import TransformException
from .split import Split
from .transform import Transform

import copy
import csv
import json

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

#   Adapt JSON reading to the CSV API
class JSONReader(object):

    def __init__(self, input, fieldnames, **config):
        self._input = input
        self.fieldnames = fieldnames

    def __iter__(self):
        return self

    def __next__(self):
        row = json.loads(next(self._input))

        result = {field: None for field in self.fieldnames}
        if isinstance(row, list):
            result.update({self.fieldnames[f]: row[f] if f < len(row) else None for f in range(len(self.fieldnames))})

        elif isinstance(row, dict):
            result.update({field: row.get(field, None) for field in self.fieldnames})

        else:
            result.update({field: row for field in self.fieldnames})

        return result

    next = __next__

readerFactory = {
    'csv': csv.DictReader,
    'json': JSONReader,
}

def bind_unnest(outputs, **kwargs):

    queue = NextAdapter()
    format = kwargs.get('format', 'csv')
    if format not in readerFactory:
        raise TransformException(f"Unknown format '{format}' for unnest")

    config = copy.copy(kwargs)
    if 'format' in config: del config['format']
    reader = readerFactory[format](queue, outputs, **config)

    def unnest(value):
        nonlocal queue, reader, outputs

        queue.append(value)

        return next(reader)

    return unnest

class Unnest(Split):
    def __init__(self, source, input, outputs, **config):
        name = 'unnest'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')

        super().__init__(source, input, outputs, bind_unnest(outputs, **config))

        self.name = name
