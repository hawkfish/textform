import unittest
from context import *

import io
import json

def generate_record(count, layout):
    outfile = io.StringIO()
    writer = txf.layouts.WriterFactory('iterate', layout, outfile, [f'{i}' for i in range(count)])
    writer.writerow([f'Value {i}' for i in range(count)])
    return outfile.getvalue()

def generate_csv(count):
    return generate_record(count, 'csv')

def generate_json_array(count):
    return json.dumps([f"Value {i}" for i in range(count)])

def generate_json_object(count):
    return generate_record(count, 'jsonl')

def generate_md(count):
    return generate_record(count, 'md')

class TestIterate(unittest.TestCase):

    def assert_iterate(self, count, generator, layout):
        config = {}
        input = 'Nested'
        tags = 'Tag'
        strings = 'String'
        outputs = (tags, strings,)
        s = txf.Add(None, input, generator(count))
        s = txf.Limit(s, 1)
        t = txf.Iterate(s, input, tags, strings, layout, **config)

        self.assertEqual('iterate', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)

        self.assertEqual(list(outputs), t.fieldnames)

        for i, output in enumerate(outputs):
            self.assertTrue(output in t.schema, output)
            self.assertEqual(str, t.getSchemaType(output), output)

        for r in range(count):
            actual = t.readrow()
            expected = {outputs[0]: str(r), outputs[1]: f'Value {r}'}
            self.assertEqual(expected, actual)
        self.assertRaises(StopIteration, t.readrow)

        return t

    def assert_iterate_csv(self, count):
        self.assert_iterate(count, generate_csv, 'csv')

    def test_iterate_csv(self):
        self.assert_iterate_csv(0)
        self.assert_iterate_csv(1)
        self.assert_iterate_csv(2)
        self.assert_iterate_csv(5)

    def assert_iterate_json_array(self, count):
        self.assert_iterate(count, generate_json_array, 'json')

    def test_iterate_json_array(self):
        self.assert_iterate_json_array(0)
        self.assert_iterate_json_array(1)
        self.assert_iterate_json_array(2)
        self.assert_iterate_json_array(19)

    def assert_iterate_json_object(self, count):
        self.assert_iterate(count, generate_json_object, 'json')

    def test_iterate_json_object(self):
        self.assert_iterate_json_object(0)
        self.assert_iterate_json_object(1)
        self.assert_iterate_json_object(2)
        self.assert_iterate_json_object(19)

    def assert_iterate_md(self, count):
        self.assert_iterate(count, generate_md, 'md')

    def test_iterate_md(self):
        self.assert_iterate_md(0)
        self.assert_iterate_md(1)
        self.assert_iterate_md(2)
        self.assert_iterate_md(11)

    def test_overwrite(self):
        text = io.StringIO('Col 1,Col 2\n')
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Iterate, s, 'Target', 'First', 'Overwrite')
