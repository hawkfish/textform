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

def expected_jsonl(header, count):
    eol = '\n'
    body = eol.join([json.dumps({header[0]: 'Value', header[1]: r}) for r in range(count)])
    if count: body += eol
    return body

def expected_md(fieldnames, count):
    sep = '|'
    def md_row(values):
        return '{}{}{}'.format(sep, sep.join(values), sep)
    expected = [md_row(fieldnames), md_row(['---',] * len(fieldnames)),]
    expected.extend([md_row(['Value', str(r)]) for r in range(count)])

    eol = '\n'
    expected = eol.join(expected)
    expected += eol

    return expected

expected_factory = {
    'csv': expected_csv,
    'json': expected_json,
    'jsonl': expected_jsonl,
    'md': expected_md,
}

class TestWrite(unittest.TestCase):

    def assert_write(self, count, format='csv'):
        config = {}
        outfile = io.StringIO(newline=None)
        s = txf.Add(None, 'String', 'Value')
        s = txf.Sequence(s, 'Row')
        s = txf.Limit(s, count)
        t = txf.Write(s, outfile, format, **config)

        self.assertEqual('write', t.name)
        self.assertEqual(('String', 'Row',), t.inputs)
        self.assertEqual(tuple(), t.outputs)
        self.assertEqual(s, t.source)

        self.assertEqual(s.schema, t.schema)
        self.assertEqual(s.fieldnames, t.fieldnames)

        self.assertEqual(count, t.pump())

        expected = expected_factory[format](t.inputs, count)
        self.assertEqual(expected, outfile.getvalue())

    def test_write_csv(self):
        self.assert_write(0)
        self.assert_write(1)
        self.assert_write(2)
        self.assert_write(19)

    def test_write_json(self):
        self.assert_write(0, 'json')
        self.assert_write(1, 'json')
        self.assert_write(2, 'json')
        self.assert_write(5, 'json')

    def test_write_jsonl(self):
        self.assert_write(0, 'jsonl')
        self.assert_write(1, 'jsonl')
        self.assert_write(2, 'jsonl')
        self.assert_write(7, 'jsonl')

    def test_write_md(self):
        self.assert_write(0, 'md')
        self.assert_write(1, 'md')
        self.assert_write(2, 'md')
        self.assert_write(11, 'md')

    def test_missing_source(self):
        self.assertRaises(txf.TransformException, txf.Write, None, None)

    def test_unknown_format(self):
        config = {'format': 'invalid'}
        s = txf.Add(None, 'String', 'Value')
        self.assertRaises(txf.TransformException, txf.Write, s, None, **config)
