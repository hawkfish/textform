'''Adapt Python object reading to the CSV API'''

# Reader would require a parser for Python object strings

class LineWriter(object):
    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def writerow(self, values):
        self._outfile.write(dict(zip(self.fieldnames, values)))

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = LineWriter(outfile)
        self.fieldnames = fieldnames

    def writeheader(self):
        pass

    def writerow(self, row):
        self.writer.writerow([row[field] for field in self.fieldnames])

    def writefooter(self):
        pass
