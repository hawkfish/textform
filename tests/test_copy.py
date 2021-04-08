import unittest
from context import *

class MockEmpty(txf.Transform):
    def next(self) : return None

class TestCopy(unittest.TestCase):

    def assert_copy(self, input, outputs, value):
        extra = 'Extra'
        s = txf.Add(None, (extra, input,), (0, value,))
        t = txf.Copy(s, input, outputs)

        self.assertEqual('copy', t.name(), )
        self.assertEqual(s, t.source())
        self.assertEqual(input, t.input())
        self.assertEqual(outputs, t.outputs())

        expected = list(s.outputs())
        expected.extend(outputs)
        self.assertEqual(expected, t.layout())

        schema = t.schema()
        self.assertEqual(2 + len(outputs), len(schema))

        self.assertTrue(extra in schema)
        self.assertEqual(int, schema[extra]['type'])

        self.assertTrue(input in schema)
        self.assertEqual(type(value), schema[input]['type'])

        row = t.next()
        for output in outputs:
            self.assertTrue(output in schema)
            self.assertEqual(schema[input]['type'], schema[output]['type'])
            self.assertEqual(row[input], row[output])

        return t

    def assert_copy_one(self, input, output, value):
        return self.assert_copy(input, (output,), value)

    def test_copy_string(self):
        self.assert_copy_one('Added', 'Clone', 'String')

    def test_copy_int(self):
        self.assert_copy_one('Added', 'Clone', 37)

    def test_copy_strings(self):
        input = 'Added'
        outputs = ('Clone 1', 'Clone 2',)
        value = 'String',
        t = self.assert_copy(input, outputs, value)

    def test_copy_ints(self):
        input = 'Added'
        outputs = ('Clone 1', 'Clone 2',)
        value = 1
        t = self.assert_copy(input, outputs, value)

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
