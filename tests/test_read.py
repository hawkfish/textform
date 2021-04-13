import unittest
from context import *

import io
import json

def generate_csv(outputs, lines):
    strings = ['Row#,String',]
    strings.extend([f'{i},"String {i}"' for i in range(lines)])
    return io.StringIO('\n'.join(strings))

def generate_jsonl(outputs, lines):
    return io.StringIO('\n'.join([json.dumps({outputs[0]: i, outputs[1]: f"String {i}"}) for i in range(lines)]))

def generate_py(outputs, lines):
    return [{outputs[0]: i, outputs[1]: f"String {i}"} for i in range(lines)]

def generate_text(outputs, lines):
    return io.StringIO('\n'.join([f"Line {i}" for i in range(lines)]))

generate_factory = {
    'csv': generate_csv,
    'json': generate_jsonl,
    'jsonl': generate_jsonl,
    'py': generate_py,
    'text': generate_text,
}

schemas = {
    'csv': (str, str,),
    'json': (int, str,),
    'jsonl': (int, str,),
    'py': (int, str,),
    'text': (str,),
}

output_cols = {
    'text': ('Text',),
}

configs = {
    'csv': {},
    'text': {'default_fieldnames': ('Text',)},
}

class TestRead(unittest.TestCase):

    def assert_read(self, lines, format='csv'):
        outputs = output_cols.get(format, ('Row#', 'String',))
        config = configs.get(format, {'default_fieldnames': ('Row#', 'String',)})
        text = generate_factory[format](outputs, lines)
        t = txf.Read(text, None, format, **config)

        self.assertEqual('read', t.name)
        self.assertIsNone(t.source)
        self.assertEqual(tuple(), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(list(outputs), t.fieldnames)

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertIsNone(t.getSchemaType(output))

        self.assertEqual(lines, t.pump())

        for i, output in enumerate(outputs):
            self.assertTrue(output in t.schema)
            self.assertEqual(schemas[format][i] if lines else None, t.getSchemaType(output))

        return t

    def test_read_csv(self):
        self.assert_read(0)
        self.assert_read(1)
        self.assert_read(2)
        self.assert_read(5)

    def test_read_json(self):
        self.assert_read(0, 'json')
        self.assert_read(1, 'json')
        self.assert_read(2, 'json')
        self.assert_read(19, 'json')

    def test_read_py(self):
        self.assert_read(0, 'py')
        self.assert_read(1, 'py')
        self.assert_read(2, 'py')
        self.assert_read(7, 'py')

    def test_read_text(self):
        self.assert_read(0, 'text')
        self.assert_read(1, 'text')
        self.assert_read(2, 'text')
        self.assert_read(11, 'text')

    def test_overwrite(self):
        text = io.StringIO('Overwrite\n')
        s = txf.Add(None, 'Overwrite', 1)
        self.assertRaises(txf.TransformException, txf.Read, text, s)
