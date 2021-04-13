'''Adapt Markdown table reading to the CSV API'''

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
    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        if fieldnames is None:
            self.fieldnames = tuple(self.readparts())
            self.readparts()
        else:
            self.fieldnames = fieldnames

    def __iter__(self):
        return self

    def readparts(self):
        #   Strip blanks on either side
        return split_escaped(next(self._iterable))[1:-1]

    def readrow(self):
        parts = self.readparts()
        return {field: parts[f] for f, field in enumerate(self.fieldnames)}

    def __next__(self):
        return self.readrow()

    next = __next__

class Writer(object):

    def __init__(self, outfile, fieldnames, **config):
        self._outfile = outfile
        self.fieldnames = fieldnames

    def _writeline(self, values):
        self._outfile.write('|')
        self._outfile.write(join_escaped(values))
        self._outfile.write('|\n')

    def writeheader(self):
        self._writeline(self.fieldnames)
        self._writeline(['---' for field in self.fieldnames])

    def writerow(self, row):
        self._writeline([row[field] for field in self.fieldnames])

    def writefooter(self):
        pass

Nester = Writer
Unnester = Reader
