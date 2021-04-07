import unittest
from context import *

class MockEmpty(txf.Transform):
    def next(self) : return None

class TestCopy(unittest.TestCase):

    def assert_construct(self, input, outputs, values):
        s = txf.Add(None, input, values)
        t = txf.Copy(s, input, outputs)

        self.assertEqual('copy', t.name(), )
        self.assertEqual(s, t.source())
        self.assertEqual(input, t.input())

        return t

    def assert_copy_one(self, input, output, value):
        t = self.assert_construct(input, output, value)

        self.assertEqual((output,), t.outputs())

        self.assertEqual({output: {'type': type(value)}, input: {'type': type(value)}}, t.schema())
        self.assertEqual({output: value, input: value}, t.next())

    def assert_copy_multiple(self, input, outputs, value):
        t = self.assert_construct(input, outputs, value)

        self.assertEqual(outputs, t.outputs())

        schema = t.schema()
        row = t.next()
        for i, output in enumerate(outputs):
            self.assertEqual(schema[input], schema[output])
            self.assertEqual(row[input], row[output])

    def test_copy_string(self):
        self.assert_copy_one('Added', 'Clone', 'String')

    def test_copy_int(self):
        self.assert_copy_one('Added', 'Clone', 37)

    def test_copy_strings(self):
        input = 'Added'
        outputs = ('Clone 1', 'Clone 2',)
        value = 'String',
        t = self.assert_copy_multiple(input, outputs, value)

    def test_copy_ints(self):
        input = 'Added'
        outputs = ('Clone 1', 'Clone 2',)
        value = 1
        t = self.assert_copy_multiple(input, outputs, value)

    def test_last_row(self):
        input = 'Added'
        t = txf.Add(MockEmpty('empty'), input, '10')
        t = txf.Copy(t, input, 'Clone')
        self.assertIsNone(t.next())

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Copy, None, 'Added', 'Clone')

    def test_missing(self):
        s = txf.Add(None, 'Added', (1,))
        self.assertRaises(txf.TransformException, txf.Copy, s, 'Missing', 'Clone')

    def test_overwrite(self):
        s = txf.Add(None, 'Added', (1,))
        self.assertRaises(txf.TransformException, txf.Copy, s, 'Added', 'Added')
