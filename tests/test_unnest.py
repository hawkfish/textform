import unittest
from context import *

import io
import json

def generate_csv(outputs, lines):
    return [f'{i},"String {i}"' for i in range(lines)]

def generate_json(outputs, lines):
    return [json.dumps({outputs[0]: i, outputs[1]: f"String {i}"}) for i in range(lines)]

generate_factory = {
    'csv': generate_csv,
    'json': generate_json,
}

class TestUnnest(unittest.TestCase):

    def assert_unnest(self, lines, format='csv'):
        config = {'format': format}
        input = 'Line'
        outputs = ('Row#', 'String',)
        text = '\n'.join(generate_factory[format](outputs, lines))
        s = txf.Text(io.StringIO(text), input)
        t = txf.Unnest(s, input, outputs, **config)

        self.assertEqual('unnest', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)

        self.assertEqual(list(outputs), t.layout)

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertEqual(str, t.schema[output]['type'])

        self.assertEqual(lines, t.pull())

        return t

    def test_unnest_csv(self):
        self.assert_unnest(0)
        self.assert_unnest(1)
        self.assert_unnest(2)
        self.assert_unnest(10)

    def test_unnest_json(self):
        self.assert_unnest(0, 'json')
        self.assert_unnest(1, 'json')
        self.assert_unnest(2, 'json')
        self.assert_unnest(10, 'json')

    def test_overwrite(self):
        text = io.StringIO('Col 1,Col 2\n')
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Unnest, s, 'Target', ('First', 'Overwrite',))
