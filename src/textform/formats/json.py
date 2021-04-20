from . import jsonl

LineReader = jsonl.LineReader
DictReader = jsonl.DictReader
LineWriter = jsonl.LineWriter

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = LineWriter(outfile, fieldnames)
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

