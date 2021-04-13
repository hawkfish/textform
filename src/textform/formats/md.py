def escape(field):
    field = str(field)
    return r'\|'.join(field.split('|'))

class Writer(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def _writeline(self, values):
        escaped = [escape(value) for value in values]
        self._outfile.write('|')
        self._outfile.write('|'.join(escaped))
        self._outfile.write('|\n')

    def writeheader(self):
        self._writeline(self.fieldnames)
        self._writeline(['---' for field in self.fieldnames])

    def writerow(self, row):
        self._writeline([row[field] for field in self.fieldnames])

    def writefooter(self):
        pass

Nester = Writer
