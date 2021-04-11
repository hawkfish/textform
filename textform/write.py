from .common import TransformException
from .transform import Transform

import csv
import json

class CSVWriter(csv.DictWriter):

    def __init__(self, outfile, fieldnames):
        super().__init__(outfile, fieldnames)
        self.writeheader()

    def writefooter(self):
        pass

class JSONWriter(object):

    def __init__(self, outfile, fieldnames):
        self._outfile = outfile
        self.fieldnames = fieldnames

        self._outfile.write('[')
        self._sep = ''

    def writerow(self, row):
        self._outfile.write(self._sep)
        self._sep = ', '
        json.dump(row, self._outfile)

    def writefooter(self):
        self._outfile.write(']')

class JSONLinesWriter(object):

    def __init__(self, outfile, fieldnames):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def writerow(self, row):
        self._outfile.write(json.dumps(row))
        self._outfile.write('\n')

    def writefooter(self):
        pass

writer_factory = {
    'csv': CSVWriter,
    'json': JSONWriter,
    'jsonl': JSONLinesWriter,
}

class Write(Transform):
    def __init__(self, source, outfile, **params):
        super().__init__('write', source.layout if source else (), (), source)

        self._requireSource()

        format = params.get('format', 'csv')
        if format not in writer_factory:
            raise TransformException(f"Unknown {self.name} format: '{format}'")

        self._writer = writer_factory[format](outfile, self.layout)

    def next(self):
        row = super().next()
        if row is not None:
            self._writer.writerow(row)
        else:
            self._writer.writefooter()

        return row
