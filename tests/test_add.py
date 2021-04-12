import unittest
from helpers import *

class TestAdd(unittest.TestCase):

    def assert_add(self, outputs, values):
        t = txf.Add(None, outputs, values)

        self.assertEqual('add', t.name, )
        self.assertIsNone(t.source)
        self.assertEqual(tuple(), t.inputs)

        self.assertEqual(outputs, t.outputs)
        self.assertEqual(values, t.values)

        schema = t.schema
        for i, output in enumerate(outputs):
            self.assertEqual({'type': type(values[i])}, schema[output])

        row = t.next()
        self.assertIsNotNone(row)
        for i, output in enumerate(outputs):
            self.assertEqual(values[i], row[output])

        return t

    def assert_add_one(self, output, value):
        return self.assert_add((output,), (value,))

    def test_add_string(self):
        self.assert_add_one('Added', 'String')

    def test_add_int(self):
        self.assert_add_one('Added', 37)

    def test_add_strings(self):
        outputs = ('Add 1', 'Add 2',)
        values = ('Thing 1', 'Thing 2',)
        t = self.assert_add(outputs, values)

    def test_add_ints(self):
        outputs = ('Add 1', 'Add 2',)
        values = (1, 2,)
        t = self.assert_add(outputs, values)

    def test_add_mixed(self):
        outputs = ('Add 1', 'Add 2',)
        values = ('Thing 1', 2,)
        t = self.assert_add(outputs, values)

    def test_last_row(self):
        t = txf.Add(MockEmpty('empty'), 'Added', 1)
        self.assertIsNone(t.next())

    def test_mismatch(self):
        self.assertRaises(txf.TransformException, txf.Add, None, ('Add 1', 'Add 2',), (2,))
        self.assertRaises(txf.TransformException, txf.Add, None, ('Added',), (1, 2,))

    def test_overwrite(self):
        s = self.assert_add_one('Overwrite', 1)
        self.assertRaises(txf.TransformException, txf.Add, s, 'Overwrite', 2)
