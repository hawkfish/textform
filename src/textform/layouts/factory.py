from . import csv
from . import json
from . import jsonl
from . import md
from . import rst
from . import text
from ..common import TransformException

def _ValidateInputFormat(name, layout, layouts, iterable):
    if layout not in layouts:
        raise TransformException(f"Unknown {name} '{layout}'")

    try:
        iterable = iter(iterable)

    except:
        raise TransformException(f"Input to {name} is not iterable")

def LineReaderFactory(name, layout, iterable, **config):

    layouts = {
        'csv': csv.LineReader,
        'json': json.LineReader,
        'jsonl': jsonl.LineReader,
        'md': md.LineReader,
        'text': text.LineReader,
    }

    _ValidateInputFormat(name, layout, layouts, iterable)

    return layouts[layout](iterable, **config)

def DictReaderFactory(name, layout, iterable, fieldnames, **config):

    layouts = {
        'csv': csv.DictReader,
        'json': json.DictReader,
        'jsonl': jsonl.DictReader,
        'md': md.DictReader,
        'text': text.DictReader,
    }

    _ValidateInputFormat(name, layout, layouts, iterable)

    return layouts[layout](iterable, fieldnames, **config)

def _ValidateOutputFormat(name, layout, layouts, outfile):
    if layout not in layouts:
        raise TransformException(f"Unknown {name} layout: '{layout}'")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

def LineWriterFactory(name, layout, outfile, fieldnames, **config):

    layouts = {
        'csv': csv.LineWriter,
        'json': json.LineWriter,
        'jsonl': jsonl.LineWriter,
        'md': md.LineWriter,
        'rst': rst.LineWriter,
        'text': text.LineWriter,
    }

    _ValidateOutputFormat(name, layout, layouts, outfile)

    return layouts[layout](outfile, fieldnames, **config)

def DictWriterFactory(name, layout, outfile, fieldnames, **config):

    layouts = {
        'csv': csv.DictWriter,
        'json': json.DictWriter,
        'jsonl': jsonl.DictWriter,
        'md': md.DictWriter,
        'rst': rst.DictWriter,
    }

    _ValidateOutputFormat(name, layout, layouts, outfile)

    return layouts[layout](outfile, fieldnames, **config)
