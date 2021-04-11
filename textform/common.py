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
            try:
                self._buffered = self.readrow()
                self.fieldnames = self._buffered.keys()
            except StopIteration:
                self.fieldnames = config.get('default_fieldnames', ())

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

def MakeLineReader(name, format, iterable, fieldnames=None, **config):

    readers = {
        'csv': csv.DictReader,
        'json': JSONReader,
        'jsonl': JSONReader,
        'py': PyReader,
        'text': TextReader,
    }

    if format not in readers:
        raise TransformException(f"Unknown format '{format}' in {name}")

    try:
        iter(iterable)
    except:
        raise TransformException(f"Input to {name} is not iterable")

    return readers[format](iterable, fieldnames, **config)

class CSVWriter(csv.DictWriter):

    def __init__(self, outfile, fieldnames, **config):
        super().__init__(outfile, fieldnames)

    def writefooter(self):
        pass

class JSONWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames
        self._sep = ''

    def writeheader(self):
        self._outfile.write('[')

    def writerow(self, row):
        self._outfile.write(self._sep)
        self._sep = ', '
        json.dump(row, self._outfile)

    def writefooter(self):
        self._outfile.write(']')

class JSONLinesWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def writeheader(self):
        pass

    def writerow(self, row):
        self._outfile.write(json.dumps(row))
        self._outfile.write('\n')

    def writefooter(self):
        pass

def MakeLineWriter(name, format, outfile, fieldnames=None, **config):

    writers = {
        'csv': CSVWriter,
        'json': JSONWriter,
        'jsonl': JSONLinesWriter,
    }

    if format not in writers:
        raise TransformException(f"Unknown {name} format: '{format}'")

    try:
        outfile.write
    except:
        raise TransformException(f"Output for {name} is not writable")

    return writers[format](outfile, fieldnames, **config)

def MakeFieldWriter(name, format, outfile, fieldnames=None, **config):
    xlate = {'json': 'jsonl'}
    return MakeLineWriter(name, xlate.get(format, format), outfile, fieldnames, **config)
