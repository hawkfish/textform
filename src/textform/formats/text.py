'''Adapt single line text files to the csv API'''

from . import dictinput

class Reader(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable

    def __next__(self):
        return str(next(self._iterable))[:-1]

    next = __next__

class DictReader(dictinput.DictInput):
    def __init__(self, iterable, fieldnames=None, **config):
        #   There is only ONE column for text input
        if not fieldnames:
            fieldnames = tuple(config.get('default_fieldnames', ('text',)))
        fieldnames = fieldnames[:1]

        super().__init__(Reader(iterable), fieldnames, **config)

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
