from . import csv
from . import json
from . import jsonl
from . import md
from . import py
from . import text
from ..common import TransformException

def InputFormatFactory(name, format, formats, iterable, fieldnames=None, **config):
    if format not in formats:
        raise TransformException(f"Unknown read format '{format}' in {name}")

    try:
        iterable = iter(iterable)
    except:
        raise TransformException(f"Input to {name} is not iterable")

    return formats[format](iterable, fieldnames, **config)

def ReaderFactory(name, format, iterable, fieldnames=None, **config):

    readers = {
        'csv': csv.Reader,
        'json': json.Reader,
        'jsonl': jsonl.Reader,
        'md': md.Reader,
        'py': py.Reader,
        'text': text.Reader,
    }

    return InputFormatFactory(name, format, readers, iterable, fieldnames, **config)

def UnnesterFactory(name, format, iterable, fieldnames=None, **config):

    unnesters = {
        'csv': csv.Unnester,
        'json': json.Unnester,
        'jsonl': jsonl.Unnester,
        'md': md.Unnester,
        'py': py.Unnester,
        'text': text.Unnester,
    }

    return InputFormatFactory(name, format, unnesters, iterable, fieldnames, **config)

def OutputFormatFactory(name, format, formats, outfile, fieldnames=None, **config):
    if format not in formats:
        raise TransformException(f"Unknown write format: '{format}' in  {name}")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

    return formats[format](outfile, fieldnames, **config)

def WriterFactory(name, format, outfile, fieldnames=None, **config):

    writers = {
        'csv': csv.Writer,
        'json': json.Writer,
        'jsonl': jsonl.Writer,
        'md': md.Writer,
        'py': py.Writer,
    }

    return OutputFormatFactory(name, format, writers, outfile, fieldnames, **config)

def NesterFactory(name, format, outfile, fieldnames=None, **config):

    nesters = {
        'csv': csv.Nester,
        'json': json.Nester,
        'jsonl': jsonl.Nester,
        'md': jsonl.Nester,
        'py': py.Nester,
    }

    return OutputFormatFactory(name, format, nesters, outfile, fieldnames, **config)
