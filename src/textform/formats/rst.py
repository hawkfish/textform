'''Adapters for the rst interface

rst has a nasty "feature" where the data is interpreted with markup.
In order to make tables that can be use with the csv-table directive
as *data*, we need to escape various things.
'''

from . import csv
import re

LineReader = csv.LineReader
DictReader = csv.DictReader

def needs_escape(s):
    return not s.isalnum()

def escape_transitions(s):
    # "Titles are underlined (or over- and underlined) with a printing nonalphanumeric 7-bit ASCII character"
    if not isinstance(s, str) or not needs_escape(s): return s

    # Find runs of four or more non-transition characters and escape them
    prev = ''
    copies = 0
    result = ''
    for c in s:
        if needs_escape(c):
            if c != prev:
                prev = c
                copies = 1

            elif copies >= 3:
                result += '\\'
                copies = 0

            else:
                copies += 1

        result += c

    return result

def escape_value(v):
    return escape_transitions(v)

class LineWriter(csv.LineWriter):

    def writerow(self, values):
        super().writerow([escape_value(value) for value in values])

class DictWriter(csv.DictWriter):

    def writerow(self, row):
        super().writerow({field: escape_value(row[field]) for field in row})
