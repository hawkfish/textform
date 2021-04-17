from . import jsonl

Reader = jsonl.Reader
DictReader = jsonl.DictReader
Writer = jsonl.Writer

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = Writer(outfile, fieldnames)
        self.fieldnames = fieldnames
        self._sep = ''

    def writeheader(self):
        self.writer.write('[')

    def writerow(self, row):
        self.writer.write(self._sep)
        self.writer.writerow([row[field] for field in self.fieldnames])
        self._sep = ', '

    def writefooter(self):
        self.writer.write(']')

