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

def ValidateInputFormat(name, layout, layouts, iterable):
    if layout not in layouts:
        raise TransformException(f"Unknown {name} '{layout}'")

    try:
        iterable = iter(iterable)

    except:
        raise TransformException(f"Input to {name} is not iterable")

def ReaderFactory(name, layout, iterable, **config):

    layouts = {
        'csv': csv.LineReader,
        'json': json.LineReader,
        'jsonl': jsonl.LineReader,
        'md': md.LineReader,
        'text': text.LineReader,
    }

    ValidateInputFormat(name, layout, layouts, iterable)

    return layouts[layout](iterable, **config)

def DictReaderFactory(name, layout, iterable, fieldnames, **config):

    layouts = {
        'csv': csv.DictReader,
        'json': json.DictReader,
        'jsonl': jsonl.DictReader,
        'md': md.DictReader,
        'text': text.DictReader,
    }

    ValidateInputFormat(name, layout, layouts, iterable)

    return layouts[layout](iterable, fieldnames, **config)

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

def ValidateOutputFormat(name, layout, layouts, outfile):
    if layout not in layouts:
        raise TransformException(f"Unknown {name} layout: '{layout}'")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

def WriterFactory(name, layout, outfile, fieldnames, **config):

    layouts = {
        'csv': csv.LineWriter,
        'json': json.LineWriter,
        'jsonl': jsonl.LineWriter,
        'md': md.LineWriter,
        'py': py.LineWriter,
        'rst': rst.LineWriter,
        'text': text.LineWriter,
    }

    ValidateOutputFormat(name, layout, layouts, outfile)

    return layouts[layout](outfile, fieldnames, **config)

def DictWriterFactory(name, layout, outfile, fieldnames, **config):

    layouts = {
        'csv': csv.DictWriter,
        'json': json.DictWriter,
        'jsonl': jsonl.DictWriter,
        'md': md.DictWriter,
        'py': py.DictWriter,
        'rst': rst.DictWriter,
    }

    ValidateOutputFormat(name, layout, layouts, outfile)

    return layouts[layout](outfile, fieldnames, **config)
