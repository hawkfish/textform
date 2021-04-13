from . import jsonl
import json

Reader = jsonl.Reader

class Writer(object):

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

Nester = jsonl.Writer
Unnester = Reader
