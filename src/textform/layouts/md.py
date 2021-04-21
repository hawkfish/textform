'''Adapt Markdown table reading to the CSV API'''

from . import dictreader

import re

def _escape(field, sep='|', esc='\\'):
    field = str(field)
    return (esc+sep).join(field.split(sep))

def _join_escaped(values, sep='|', esc='\\'):
    return '|'.join([_escape(value, sep, esc) for value in values])

def _split_escaped(field, sep='|', esc='\\'):
    #   No slick Python way, we have to write a state machine
    parts = []
    state = 0
    part = ''
    for c in field:
        if state == 0:
            if c == sep:
                parts.append(part)
                part = ''
            elif c == esc:
                state = 1
            else:
                part += c

        elif state == 1:
            part += c
            state = 0

    parts.append(part)

    return parts

class LineReader(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable

        #   Header punctuation characters
        self._pat = re.compile(f"[^-* ]")

    def isdata(self, values):
        return max([1 if self._pat.search(value) else 0 for value in values])

    def __next__(self):
        values = _split_escaped(next(self._iterable))[1:-1]
        while not self.isdata(values):
            values = _split_escaped(next(self._iterable))[1:-1]

        return values

    next = __next__

class DictReader(dictreader.DictReader):

    def __init__(self, iterable, fieldnames=None, **config):
        super().__init__(LineReader(iterable), fieldnames, **config)

class LineWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile

    def write(self, s):
        self._outfile.write(s)

    def writerow(self, values):
        self.write('|')
        self.write(_join_escaped(values))
        self.write('|')

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = LineWriter(outfile, fieldnames)
        self.fieldnames = fieldnames

    def writeheader(self):
        self.writer.writerow(self.fieldnames)
        self.writer.write('\n')
        self.writer.writerow(['---' for field in self.fieldnames])
        self.writer.write('\n')

    def writerow(self, row):
        self.writer.writerow([row[field] for field in self.fieldnames])
        self.writer.write('\n')

    def writefooter(self):
        pass
