import unittest
from context import *

import io
import json

def generate_csv(outputs, lines):
    return io.StringIO('\n'.join([f'{i},"String {i}"' for i in range(lines)]))

def generate_json(outputs, lines):
    return io.StringIO('\n'.join([json.dumps({outputs[0]: i, outputs[1]: f"String {i}"}) for i in range(lines)]))

def generate_py(outputs, lines):
    return iter([{outputs[0]: i, outputs[1]: f"String {i}"} for i in range(lines)])

generate_factory = {
    'csv': generate_csv,
    'json': generate_json,
    'jsonl': generate_json,
    'py': generate_py,
}

schemas = {
    'csv': (str, str,),
    'json': (int, str,),
    'jsonl': (int, str,),
    'py': (int, str,),
}

class TestUnnest(unittest.TestCase):

    def assert_unnest(self, lines, format='csv'):
        config = {}
        input = 'Line'
        outputs = ('Row#', 'String',)
        text = generate_factory[format](outputs, lines)
        s = txf.Text(text, input)
        t = txf.Unnest(s, input, outputs, format, **config)

        self.assertEqual('unnest', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)

        self.assertEqual(list(outputs), t.layout)

        for i, output in enumerate(outputs):
            self.assertTrue(output in t.schema, output)
            self.assertIsNone(t.getSchemaType(output), output)

        for expected in generate_py(outputs, lines):
            row = t.next()
            self.assertIsNotNone(row)
            for i, output in enumerate(outputs):
                cast = schemas[format][i]
                self.assertEqual(cast(expected[output]), row[output], output)
        self.assertIsNone(t.next())

        for i, output in enumerate(outputs):
            self.assertTrue(output in t.schema, output)
            self.assertEqual(schemas[format][i] if lines else None, t.schema[output]['type'], output)

        return t

    def test_unnest_csv(self):
        self.assert_unnest(0)
        self.assert_unnest(1)
        self.assert_unnest(2)
        self.assert_unnest(5)

    def test_unnest_json(self):
        self.assert_unnest(0, 'json')
        self.assert_unnest(1, 'json')
        self.assert_unnest(2, 'json')
        self.assert_unnest(19, 'json')

    def test_unnest_py(self):
        self.assert_unnest(0, 'py')
        self.assert_unnest(1, 'py')
        self.assert_unnest(2, 'py')
        self.assert_unnest(7, 'py')

    def test_overwrite(self):
        text = io.StringIO('Col 1,Col 2\n')
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Unnest, s, 'Target', ('First', 'Overwrite',))
