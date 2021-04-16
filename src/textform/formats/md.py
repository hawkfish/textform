'''Adapt Markdown table reading to the CSV API'''

from . import dictinput

import re

def escape(field, sep='|', esc='\\'):
    field = str(field)
    return (esc+sep).join(field.split(sep))

def join_escaped(values, sep='|', esc='\\'):
    return '|'.join([escape(value, sep, esc) for value in values])

def split_escaped(field, sep='|', esc='\\'):
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

class Reader(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable

        self._pat = re.compile(f"[^-]")

    def isdata(self, values):
        return max([1 if self._pat.search(value) else 0 for value in values])

    def __next__(self):
        values = split_escaped(next(self._iterable))[1:-1]
        while not self.isdata(values):
            values = split_escaped(next(self._iterable))[1:-1]

        return values

    next = __next__

class DictReader(dictinput.DictInput):

    def __init__(self, iterable, fieldnames=None, **config):
        super().__init__(Reader(iterable), fieldnames, **config)

class Writer(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile

    def writerow(self, values):
        self._outfile.write('|')
        self._outfile.write(join_escaped(values))
        self._outfile.write('|\n')

class DictWriter(object):

    def __init__(self, outfile, fieldnames, **config):
        self.writer = Writer(outfile, fieldnames)
        self.fieldnames = fieldnames

    def writeheader(self):
        self.writer.writerow(self.fieldnames)
        self.writer.writerow(['---' for field in self.fieldnames])

    def writerow(self, row):
        self.writer.writerow([row[field] for field in self.fieldnames])

    def writefooter(self):
        pass
