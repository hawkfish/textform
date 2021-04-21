'''Adapt single line text files to the csv API'''

from . import dictreader

class LineReader(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable

    def __next__(self):
        return str(next(self._iterable))[:-1]

    next = __next__

class DictReader(dictreader.DictReader):
    def __init__(self, iterable, fieldnames=None, **config):
        #   There is only ONE column for text input
        if not fieldnames:
            fieldnames = tuple(config.get('default_fieldnames', ('text',)))
        fieldnames = fieldnames[:1]

        super().__init__(LineReader(iterable), fieldnames, **config)

class LineWriter(object):
    def __init__(self, outfile, **config):
        self._outfile = outfile

    def write(self, s):
        self._outfile.write(s)

    def writerow(self, values):
        self._outfile.write(str(values))

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = LineWriter(outfile, fieldnames)
        self.fieldnames = fieldnames

    def writeheader(self):
        pass

    def writerow(self, row):
        #   Slice the row
        self.writer.writerow([row[field] for field in self.fieldnames])
        self.writer.write('\n')

    def writefooter(self):
        pass

