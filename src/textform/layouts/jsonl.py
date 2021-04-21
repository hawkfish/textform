import json
from . import dictreader

#   Adapt JSON reading to the CSV API
class LineReader(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable

    def __next__(self):
        return json.loads(next(self._iterable))

    next = __next__

class DictReader(dictreader.DictReader):
    def __init__(self, iterable, fieldnames=None, **config):
        super().__init__(LineReader(iterable), fieldnames, **config)

class LineWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def write(self, s):
        self._outfile.write(s)

    def writerow(self, values):
        self.write(json.dumps(dict(zip(self.fieldnames, values))))

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

