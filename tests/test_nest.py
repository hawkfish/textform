import unittest
from context import *

import json

def expected_csv(inputs, lines):
    return [f'{i},String {i}' for i in range(lines)]

def expected_json(inputs, lines):
    return [json.dumps({inputs[0]: i, inputs[1]: f"String {i}"}) for i in range(lines)]

def expected_py(inputs, lines):
    return [{inputs[0]: i, inputs[1]: f"String {i}"} for i in range(lines)]

expected_factory = {
    'csv': expected_csv,
    'json': expected_json,
    'jsonl': expected_json,
    'py': expected_py,
}

schemas = {
    'csv': str,
    'json': str,
    'jsonl': str,
    'py': dict,
}

class TestNest(unittest.TestCase):

    def assert_nest(self, lines, format='csv'):
        output = 'Record'
        inputs = ('Row#', 'String',)
        iterable = iter([{inputs[0]: i, inputs[1]: f"String {i}"} for i in range(lines)])
        config = {'default_fieldnames': inputs}
        s = txf.Read(iterable, None, 'py', **config)
        self.assertEqual(inputs, s.outputs)
        t = txf.Nest(s, inputs, output, format)

        self.assertEqual('nest', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual(inputs, t.inputs)
        self.assertEqual((output,), t.outputs)

        self.assertEqual(output, t.output)

        self.assertEqual([output,], t.layout)

        expected = expected_factory[format](inputs, lines)
        for e in expected:
            self.assertEqual(e, t.next()[output])
        self.assertIsNone(t.next())

        self.assertTrue(output in t.schema)
        self.assertEqual(schemas[format] if lines else None, t.schema[output]['type'])

        return t

    def test_nest_csv(self):
        self.assert_nest(0)
        self.assert_nest(1)
        self.assert_nest(2)
        self.assert_nest(5)

    def test_nest_json(self):
        self.assert_nest(0, 'jsonl')
        self.assert_nest(1, 'jsonl')
        self.assert_nest(2, 'jsonl')
        self.assert_nest(19, 'jsonl')

    def test_nest_json(self):
        self.assert_nest(0, 'py')
        self.assert_nest(1, 'py')
        self.assert_nest(2, 'py')
        self.assert_nest(7, 'py')

    def test_overwrite(self):
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Nest, s, 'Target', ('First', 'Overwrite',))
