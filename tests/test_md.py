import unittest
from context import *

import io

class TestMarkDown(unittest.TestCase):

    def assert_writeheader(self, fieldnames, lines):
        expected = '\n'.join(lines) + '\n'
        outfile = io.StringIO()
        w = txf.formats.md.Writer(outfile, fieldnames)
        w.writeheader()

        actual = outfile.getvalue()
        self.assertEqual(expected, actual)

    def test_writeheader_one(self):
        fieldnames = ('Header1',)
        lines = ('|Header1|', '|---|',)
        self.assert_writeheader(fieldnames, lines)

    def test_writeheader_three(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        lines = (r'|Header1|Header2|Header3|', '|---|---|---|',)
        self.assert_writeheader(fieldnames, lines)

    def test_writeheader_vbars(self):
        fieldnames = ('Header | 1', 'Header | 2', 'Header | 3',)
        lines = (r'|Header \| 1|Header \| 2|Header \| 3|', '|---|---|---|',)
        self.assert_writeheader(fieldnames, lines)

    def assert_writerow(self, fieldnames, row, expected):
        outfile = io.StringIO()
        w = txf.formats.md.Writer(outfile, fieldnames)
        w.writerow(row)

        actual = outfile.getvalue()
        self.assertEqual(expected + '\n', actual)

    def test_writerow_one(self):
        fieldnames = ('F1',)
        row = {'F1': 1}

        self.assert_writerow(fieldnames, row, r'|1|')

    def test_writerow_three(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        row = {'Header1': 'String', 'Header2': 5, 'Header3' : 4.25,}

        self.assert_writerow(fieldnames, row, r'|String|5|4.25|')

    def test_writerow_vbars(self):
        fieldnames = ('Header1', 'Header2', 'Header3',)
        row = {'Header1': '|String|', 'Header2': 5, 'Header3' : 4.25,}

        self.assert_writerow(fieldnames, row, r'|\|String\||5|4.25|')
