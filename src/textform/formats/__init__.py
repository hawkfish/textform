from . import csv
from . import json
from . import jsonl
from . import md
from . import py
from . import rst
from . import text
from ..common import TransformException

#   deque doesn't like to be modified while iterating
class ReaderIterator(object):

    def __init__(self):
        self.buffer = None
        self.buffered = False

    def __iter__(self):
        return self

    def append(self, value):
        self.buffer = value
        self.buffered = True

    def __next__(self):
        if not self.buffered: raise StopIteration("ReaderIterator")

        result = self.buffer
        self.buffered = False
        return result

    next = __next__

def ValidateInputFormat(name, format, formats, iterable):
    if format not in formats:
        raise TransformException(f"Unknown {name} '{format}'")

    try:
        iterable = iter(iterable)

    except:
        raise TransformException(f"Input to {name} is not iterable")

def ReaderFactory(name, format, iterable, **config):

    formats = {
        'csv': csv.Reader,
        'json': json.Reader,
        'jsonl': jsonl.Reader,
        'md': md.Reader,
        'text': text.Reader,
    }

    ValidateInputFormat(name, format, formats, iterable)

    return formats[format](iterable, **config)

def DictReaderFactory(name, format, iterable, fieldnames, **config):

    formats = {
        'csv': csv.DictReader,
        'json': json.DictReader,
        'jsonl': jsonl.DictReader,
        'md': md.DictReader,
        'text': text.DictReader,
    }

    return formats[format](iterable, fieldnames, **config)

class WriterIterator(object):

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
        if not self.buffered:
            raise StopIteration("WriterIterator")

        result = self.buffer
        self.buffered = False

        return result

    next = __next__

def ValidateOutputFormat(name, format, formats, outfile):
    if format not in formats:
        raise TransformException(f"Unknown {name} format: '{format}'")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

def WriterFactory(name, format, outfile, fieldnames, **config):

    formats = {
        'csv': csv.Writer,
        'json': json.Writer,
        'jsonl': jsonl.Writer,
        'md': md.Writer,
        'py': py.Writer,
        'rst': rst.Writer,
        'text': text.Writer,
    }

    ValidateOutputFormat(name, format, formats, outfile)

    return formats[format](outfile, fieldnames, **config)

def DictWriterFactory(name, format, outfile, fieldnames, **config):

    formats = {
        'csv': csv.DictWriter,
        'json': json.DictWriter,
        'jsonl': jsonl.DictWriter,
        'md': md.DictWriter,
        'py': py.DictWriter,
        'rst': rst.DictWriter,
    }

    ValidateOutputFormat(name, format, formats, outfile)

    return formats[format](outfile, fieldnames, **config)
