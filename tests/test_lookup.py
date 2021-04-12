import unittest
from helpers import *

class TestLookup(unittest.TestCase):

    def assert_lookup(self, table):
        input = 'Column'
        value = 'String'
        default = 'Default'

        s = txf.Add(None, input, value)
        t = txf.Lookup(s, input, table, default)

        self.assertEqual('lookup', t.name, )
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(table, t.table)
        self.assertEqual(default, t.default)

        self.assertTrue(input in t.schema)
        self.assertEqual(type(default), t.getSchemaType(input))
        self.assertEqual({input: table.get(value, default)}, t.next())

        return t

    def test_lookup_found(self):
        self.assert_lookup({'String': 'Replace'})

    def test_lookup_not_found(self):
        self.assert_lookup({'Missing': 'Replace'})

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Lookup, None, 'Target', {}, '')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lookup, s, ('Target', 'Target',), {}, '')
        self.assertRaises(txf.TransformException, txf.Lookup, s, (), {}, '')

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lookup, s, 'Missing', {}, '')

    def test_mismatch(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lookup, s, 'Target', {'String': 'str'}, 5)
