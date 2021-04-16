import unittest
from context import *

import io

class TestMarkDown(unittest.TestCase):

    def assert_header(self, fieldnames, lines):
        expected = '\n'.join(lines) + '\n'
        outfile = io.StringIO()
        w = txf.formats.md.DictWriter(outfile, fieldnames)
        w.writeheader()

        actual = outfile.getvalue()
        self.assertEqual(expected, actual)

        outfile.seek(0)
        r = txf.formats.md.DictReader(outfile)
        self.assertEqual(fieldnames, r.fieldnames)

    def test_header_one(self):
        fieldnames = ('Header1',)
        lines = ('|Header1|', '|---|',)
        self.assert_header(fieldnames, lines)

    def test_header_three(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        lines = (r'|Header1|Header2|Header3|', '|---|---|---|',)
        self.assert_header(fieldnames, lines)

    def test_header_vbars(self):
        fieldnames = ('Header | 1', 'Header | 2', 'Header | 3',)
        lines = (r'|Header \| 1|Header \| 2|Header \| 3|', '|---|---|---|',)
        self.assert_header(fieldnames, lines)

    def assert_row(self, fieldnames, row, expected):
        outfile = io.StringIO()
        w = txf.formats.md.DictWriter(outfile, fieldnames)
        w.writerow(row)

        actual = outfile.getvalue()
        self.assertEqual(expected + '\n', actual)

        outfile.seek(0)
        r = txf.formats.md.DictReader(outfile, fieldnames)
        expected = {field: str(row[field]) for field in fieldnames}
        actual = next(r)
        self.assertEqual(expected, actual)

    def test_row_one(self):
        fieldnames = ('F1',)
        row = {'F1': 1}

        self.assert_row(fieldnames, row, r'|1|')

    def test_row_three(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        row = {'Header1': 'String', 'Header2': 5, 'Header3' : 4.25,}

        self.assert_row(fieldnames, row, r'|String|5|4.25|')

    def test_row_vbars(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        row = {'Header1': '|String|', 'Header2': 5, 'Header3' : 4.25,}

        self.assert_row(fieldnames, row, r'|\|String\||5|4.25|')

