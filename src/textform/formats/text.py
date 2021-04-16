'''Adapt single line text files to the csv API'''

from . import py

class Reader(object):

    def __init__(self, iterable, **config):
        self._iterable = py.Reader(iterable)

    def __next__(self):
        return str(next(self._iterable))

    next = __next__

class DictReader(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        #   There is only ONE column for text input
        self.fieldnames = fieldnames
        if not self.fieldnames:
            self.fieldnames = tuple(config.get('default_fieldnames', ('text',)))
        self.fieldnames = self.fieldnames[:1]

    def __next__(self):
        return {self.fieldnames[0]: str(next(self._iterable))}

    next = __next__

class Writer(object):
    def __init__(self, outfile, **config):
        self._outfile = outfile

    def writerow(self, values):
        self._outfile.write(str(values))

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = Writer(outfile)
        self.fieldnames = fieldnames[:1]

    def writeheader(self):
        pass

    def writerow(self, row):
        self.writer.writerow(row)

    def writefooter(self):
        pass
