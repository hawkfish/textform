import unittest
from context import *

class TestDrop(unittest.TestCase):

    def assert_construct(self, drops, inputs, values):
        s = txf.Add(None, inputs, values)
        t = txf.Drop(s, drops)

        self.assertEqual('drop', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual(tuple(), t.outputs)

        expected = list(filter(lambda input: input not in drops, inputs))
        self.assertEqual(expected, t.fieldnames)

        return t

    def assert_drop_all_one(self, input, value):
        t = self.assert_construct(input, input, value)

        self.assertEqual((input,), t.inputs)

        self.assertEqual({}, t.schema)
        self.assertEqual({}, t.readrow())

    def assert_drop_all_multiple(self, inputs, values):
        t = self.assert_construct(inputs, inputs, values)

        self.assertEqual(inputs, t.inputs)

        self.assertEqual({}, t.schema)
        self.assertEqual({}, t.readrow())

    def assert_drop_first_multiple(self, inputs, values):
        drops = inputs[:1]
        t = self.assert_construct(drops, inputs, values)

        self.assertEqual(drops, t.inputs)

        for i, input in enumerate(inputs[1:]):
            self.assertEqual(type(values[i+1]), t.getSchemaType(input), input)
        self.assertEqual({input: values[i+1] for (i, input) in enumerate(inputs[1:])}, t.readrow())

    def test_drop_string(self):
        self.assert_drop_all_one('Added', 'String')

    def test_drop_int(self):
        self.assert_drop_all_one('Added', 37)

    def test_drop_strings(self):
        inputs = ('Add 1', 'Add 2',)
        values = ('Thing 1', 'Thing 2',)
        self.assert_drop_all_multiple(inputs, values)
        self.assert_drop_first_multiple(inputs, values)

    def test_drop_ints(self):
        inputs = ('Add 1', 'Add 2',)
        values = (1, 2,)
        self.assert_drop_all_multiple(inputs, values)
        self.assert_drop_first_multiple(inputs, values)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Drop, None, 'Added')

    def test_missing(self):
        s = txf.Add(None, 'Added', (1,))
        self.assertRaises(txf.TransformException, txf.Drop, s, 'Missing')
