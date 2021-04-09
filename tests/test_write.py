import unittest
from context import *

import io

class TestWrite(unittest.TestCase):

    def assert_write(self, count):
        outfile = io.StringIO(newline=None)
        s = txf.Add(None, 'String', 'Value')
        s = txf.Sequence(s, 'Row')
        s = txf.Limit(s, count)
        t = txf.Write(s, outfile)

        self.assertEqual('write', t.name, )
        self.assertEqual(('String', 'Row',), t.inputs)
        self.assertEqual(tuple(), t.outputs)
        self.assertEqual(s, t.source)

        self.assertEqual(s.schema(), t.schema())
        self.assertEqual(s.layout(), t.layout())

        self.assertEqual(count, t.pull())

        sep = ','
        eol = '\n'
        expected = [sep.join(['String', 'Row']),]
        expected.extend([sep.join(['Value', str(r)]) for r in range(count)])
        expected = eol.join(expected)
        expected += eol
        self.assertEqual(expected, outfile.getvalue())

    def test_write_empty(self):
        self.assert_write(0)

    def test_write_one(self):
        self.assert_write(1)

    def test_write(self):
        self.assert_write(19)

    def test_missing_source(self):
        self.assertRaises(txf.TransformException, txf.Write, None, None)
