#   Adapt Python object reading to the CSV API
class Reader(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        self.fieldnames = fieldnames
        self._buffered = None
        if self.fieldnames is None:
            try:
                self._buffered = self.readrow()
                self.fieldnames = tuple(self._buffered.keys())
            except StopIteration:
                self.fieldnames = tuple(config.get('default_fieldnames', ()))

    def __iter__(self):
        return self

    def readnext(self):
        return next(self._iterable)

    def readrow(self):
        if self._buffered:
            result = self._buffered
            self._buffered = None
            return result

        return self.readnext()

    def __next__(self):
        row = self.readrow()

        result = {field: None for field in self.fieldnames}
        if isinstance(row, list):
            result.update({self.fieldnames[f]: row[f] if f < len(row) else None for f in range(len(self.fieldnames))})

        elif isinstance(row, dict):
            result.update({field: row.get(field, None) for field in self.fieldnames})

        else:
            result.update({field: row for field in self.fieldnames})

        return result

    next = __next__

class Writer(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def writeheader(self):
        pass

    def writerow(self, row):
        self._outfile.write(row)

    def writefooter(self):
        pass

Unnester = Reader
Nester = Writer
