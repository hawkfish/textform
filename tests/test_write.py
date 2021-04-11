import unittest
from context import *

import io
import json

def expected_csv(header, count):
    sep = ','
    eol = '\n'
    expected = [sep.join(header),]
    expected.extend([sep.join(['Value', str(r)]) for r in range(count)])
    expected = eol.join(expected)
    expected += eol

    return expected

def expected_json(header, count):
    return json.dumps([{header[0]: 'Value', header[1]: r} for r in range(count)])

expected_factory = {
    'csv': expected_csv,
    'json': expected_json,
}

class TestWrite(unittest.TestCase):

    def assert_write(self, count, format='csv'):
        config = {'format': format}
        outfile = io.StringIO(newline=None)
        s = txf.Add(None, 'String', 'Value')
        s = txf.Sequence(s, 'Row')
        s = txf.Limit(s, count)
        t = txf.Write(s, outfile, **config)

        self.assertEqual('write', t.name, )
        self.assertEqual(('String', 'Row',), t.inputs)
        self.assertEqual(tuple(), t.outputs)
        self.assertEqual(s, t.source)

        self.assertEqual(s.schema, t.schema)
        self.assertEqual(s.layout, t.layout)

        self.assertEqual(count, t.pull())

        expected = expected_factory[format](t.inputs, count)
        self.assertEqual(expected, outfile.getvalue())

    def test_write_csv(self):
        self.assert_write(0)
        self.assert_write(1)
        self.assert_write(19)

    def test_write_json(self):
        self.assert_write(2, 'json')

    def test_missing_source(self):
        self.assertRaises(txf.TransformException, txf.Write, None, None)
