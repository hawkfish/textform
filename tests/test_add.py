import unittest
from context import *

class MockEmpty(txf.Transform):
    def next(self) : return None

class TestAdd(unittest.TestCase):

    def assert_construct(self, outputs, values):
        t = txf.Add(None, outputs, values)

        self.assertEqual('add', t.name, )
        self.assertIsNone(t.source)
        self.assertEqual(tuple(), t.inputs)

        return t

    def assert_add_one(self, output, value):
        t = self.assert_construct(output, value)

        self.assertEqual((output,), t.outputs)
        self.assertEqual((value,), t.values)

        self.assertEqual({output: {'type': type(value)} }, t.schema())
        self.assertEqual({output: value }, t.next())

    def assert_add_multiple(self, outputs, values):
        t = self.assert_construct(outputs, values)

        self.assertEqual(outputs, t.outputs)
        self.assertEqual(values, t.values)

        schema = t.schema()
        row = t.next()
        for i, output in enumerate(outputs):
            value = values[i]
            self.assertEqual({'type': type(value)}, schema[output])
            self.assertEqual(value, row[output])

    def test_add_string(self):
        self.assert_add_one('Added', 'String')

    def test_add_int(self):
        self.assert_add_one('Added', 37)

    def test_add_strings(self):
        outputs = ('Add 1', 'Add 2',)
        values = ('Thing 1', 'Thing 2',)
        t = self.assert_add_multiple(outputs, values)

    def test_add_ints(self):
        outputs = ('Add 1', 'Add 2',)
        values = (1, 2,)
        t = self.assert_add_multiple(outputs, values)

    def test_add_mixed(self):
        outputs = ('Add 1', 'Add 2',)
        values = ('Thing 1', 2,)
        t = self.assert_add_multiple(outputs, values)

    def test_last_row(self):
        t = txf.Add(MockEmpty('empty'), 'Added', 1)
        self.assertIsNone(t.next())

    def test_mismatch(self):
        self.assertRaises(txf.TransformException, txf.Add, None, ('Add 1', 'Add 2',), (2,))
        self.assertRaises(txf.TransformException, txf.Add, None, ('Added',), (1, 2,))

    def test_overwrite(self):
        s = self.assert_construct('Overwrite', 1)
        self.assertRaises(txf.TransformException, txf.Add, s, 'Overwrite', 2)
