import json
from . import py

#   Adapt JSON reading to the CSV API
class Reader(py.Reader):

    def readnext(self):
        return json.loads(super().readnext())

class Writer(object):

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

Nester = Writer
Unnester = Reader
