import unittest
from context import *

import io

class TestRestructuredText(unittest.TestCase):

    def assert_row(self, fieldnames, row, expected):
        outfile = io.StringIO()
        w = txf.formats.rst.DictWriter(outfile, fieldnames)
        w.writerow(row)

        actual = outfile.getvalue()
        self.assertEqual(expected + '\n', actual)

    def test_one_row_unescaped(self):
        fieldnames = ('F1',)
        row = {'F1': 'abc'}

        self.assert_row(fieldnames, row, r'abc')

    def test_one_row_escaped(self):
        fieldnames = ('F1',)
        row = {'F1': '----'}

        self.assert_row(fieldnames, row, '---\\-')

    def test_one_row_mixed(self):
        fieldnames = ('F1',)
        row = {'F1': '--$$^^^^'}

        self.assert_row(fieldnames, row, '--$$^^^\\^')

    def test_one_row_long(self):
        fieldnames = ('F1',)
        row = {'F1': '------------------'}

        self.assert_row(fieldnames, row, '---\\----\\----\\----\\---')
