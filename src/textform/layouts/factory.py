from . import csv
from . import json
from . import jsonl
from . import md
from . import rst
from . import text
from ..common import TransformException

_layouts = {
    'LineReader': {
        'csv': csv.LineReader,
        'json': json.LineReader,
        'jsonl': jsonl.LineReader,
        'md': md.LineReader,
        'text': text.LineReader,
    },

    'DictReader': {
        'csv': csv.DictReader,
        'json': json.DictReader,
        'jsonl': jsonl.DictReader,
        'md': md.DictReader,
        'text': text.DictReader,
    },

    'LineWriter': {
        'csv': csv.LineWriter,
        'json': json.LineWriter,
        'jsonl': jsonl.LineWriter,
        'md': md.LineWriter,
        'rst': rst.LineWriter,
        'text': text.LineWriter,
    },

    'DictWriter': {
        'csv': csv.DictWriter,
        'json': json.DictWriter,
        'jsonl': jsonl.DictWriter,
        'md': md.DictWriter,
        'rst': rst.DictWriter,
    },
}

def GetLayout(layout):
    result = {}
    for factory in _layouts:
        if layout in _layouts[factory]:
            result[factory] = _layouts[factory][layout]
    return result

def RegisterLayout(layout, namespace):
    contents = dir(namespace)
    for factory in _layouts:
        if factory in contents:
            _layouts[factory][layout] = getattr(namespace, factory)

def UnregisterLayout(layout):
    for factory in _layouts:
        if layout in _layouts[factory]:
            del _layouts[factory][layout]

def _ValidateInputFormat(name, layout, _layouts, iterable):
    if layout not in _layouts:
        raise TransformException(f"Unknown {name} '{layout}'")

    try:
        iterable = iter(iterable)

    except:
        raise TransformException(f"Input to {name} is not iterable")

def LineReaderFactory(name, layout, iterable, **config):

    readers = _layouts['LineReader']

    _ValidateInputFormat(name, layout, readers, iterable)

    return readers[layout](iterable, **config)

def DictReaderFactory(name, layout, iterable, fieldnames, **config):

    readers = _layouts['DictReader']

    _ValidateInputFormat(name, layout, readers, iterable)

    return readers[layout](iterable, fieldnames, **config)

def _ValidateOutputFormat(name, layout, _layouts, outfile):
    if layout not in _layouts:
        raise TransformException(f"Unknown {name} layout: '{layout}'")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

def LineWriterFactory(name, layout, outfile, fieldnames, **config):

    readers = _layouts['LineWriter']

    _ValidateOutputFormat(name, layout, readers, outfile)

    return readers[layout](outfile, fieldnames, **config)

def DictWriterFactory(name, layout, outfile, fieldnames, **config):

    readers = _layouts['DictWriter']

    _ValidateOutputFormat(name, layout, readers, outfile)

    return readers[layout](outfile, fieldnames, **config)
