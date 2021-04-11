import copy
import csv
import json

class TransformException(Exception):
    pass

#   Adapt Python object reading to the CSV API
class PyReader(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        self.fieldnames = fieldnames
        self._buffered = None
        if self.fieldnames is None:
            self._buffered = self.readrow(self._fp)
            self.fieldnames = self._buffered.keys()

    def __iter__(self):
        return self

    def readnext(self):
        return next(self._iterable)

    def readrow(self):
        if self._buffered:
            result = self._buffered
            self._buffered = None
            return result

        return self.readnext()

    def __next__(self):
        row = self.readrow()

        result = {field: None for field in self.fieldnames}
        if isinstance(row, list):
            result.update({self.fieldnames[f]: row[f] if f < len(row) else None for f in range(len(self.fieldnames))})

        elif isinstance(row, dict):
            result.update({field: row.get(field, None) for field in self.fieldnames})

        else:
            result.update({field: row for field in self.fieldnames})

        return result

    next = __next__

#   Adapt JSON reading to the CSV API
class JSONReader(PyReader):

    def readnext(self):
        return json.loads(super().readnext())

class TextReader(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        self.fieldnames = fieldnames
        if not self.fieldnames:
            self.fieldnames = config['fieldnames']
        self.fieldnames = self.fieldnames[:1]

    def __iter__(self):
        return self;

    def __next__(self):
        return {self.fieldnames[0]: next(self._iterable)}

    next = __next__

def MakeLineReader(name, iterable, fieldnames=None, **params):

    readers = {
        'csv': csv.DictReader,
        'json': JSONReader,
        'jsonl': JSONReader,
        'py': PyReader,
        'text': TextReader,
    }

    try:
        iter(iterable)
    except:
        raise TransformException(f"Input to {name} is not iterable")

    format = params.get('format', 'csv')
    if format not in readers:
        raise TransformException(f"Unknown format '{format}' in {name}")

    config = copy.copy(params)
    if 'format' in config: del config['format']

    return readers[format](iterable, fieldnames, **config)

