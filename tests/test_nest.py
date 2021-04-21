import unittest
from context import *
from helpers import MockRead

import json

def expected_csv(fieldnames, count):
    return [f'{i},String {i}' for i in range(count)]

def expected_json(fieldnames, count):
    return [json.dumps({fieldnames[0]: i, fieldnames[1]: f"String {i}"}) for i in range(count)]

def expected_md(fieldnames, count):
    sep = '|'
    def md_row(values):
        return '{}{}{}'.format(sep, sep.join(values), sep)
    return [md_row([str(i), f"String {i}"]) for i in range(count)]

expected_factory = {
    'csv': expected_csv,
    'json': expected_json,
    'jsonl': expected_json,
    'md': expected_md,
}

schemas = {
    'csv': str,
    'json': str,
    'jsonl': str,
    'md': str,
    'py': dict,
}

class TestNest(unittest.TestCase):

    def assert_nest(self, count, layout='csv'):
        output = 'Record'
        inputs = ('Row#', 'String',)
        iterable = iter([{inputs[0]: i, inputs[1]: f"String {i}"} for i in range(count)])
        config = {'default_fieldnames': inputs}
        s = MockRead(iterable, inputs)
        self.assertEqual(inputs, s.outputs)
        t = txf.Nest(s, inputs, output, layout)

        self.assertEqual('nest', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual(inputs, t.inputs)
        self.assertEqual((output,), t.outputs)

        self.assertEqual(output, t.output)

        self.assertEqual([output,], t.fieldnames)

        self.assertTrue(output in t.schema)
        self.assertIsNone(t.getSchemaType(output))

        expected = expected_factory[layout](inputs, count)
        for e in expected:
            self.assertEqual(e, t.readrow()[output])
            self.assertTrue(output in t.schema)
            self.assertEqual(schemas[layout], t.getSchemaType(output))

        self.assertRaises(StopIteration, t.readrow)

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

    def test_nest_md(self):
        self.assert_nest(0, 'md')
        self.assert_nest(1, 'md')
        self.assert_nest(2, 'md')
        self.assert_nest(11, 'md')

    def test_overwrite(self):
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Nest, s, ('First', 'Overwrite',), 'Target')
