import unittest
from helpers import *

class TestCopy(unittest.TestCase):

    def assert_copy(self, input, outputs, value):
        left = 'Left'
        right = 'Right'
        s = txf.Add(None, (left, input, right,), (0, value, 1,))
        t = txf.Copy(s, input, outputs)

        self.assertEqual('copy', t.name, )
        self.assertEqual(s, t.source)
        self.assertEqual(input, t.input)
        self.assertEqual(outputs, t.outputs)

        expected = list(s.outputs)
        expected[2:2] = list(outputs)
        self.assertEqual(expected, t.fieldnames)

        self.assertEqual(3 + len(outputs), len(t.schema))

        self.assertTrue(left in t.schema)
        self.assertEqual(int, t.getSchemaType(left))

        self.assertTrue(right in t.schema)
        self.assertEqual(int, t.getSchemaType(right))

        self.assertTrue(input in t.schema)
        self.assertEqual(type(value), t.getSchemaType(input))

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertEqual(t.getSchemaType(input), t.getSchemaType(output))

        row = t.readrow()
        for output in outputs:
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
        self.assertRaises(StopIteration, t.readrow)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Copy, None, 'Added', 'Clone')

    def test_missing(self):
        s = txf.Add(None, 'Added', (1,))
        self.assertRaises(txf.TransformException, txf.Copy, s, 'Missing', 'Clone')

    def test_overwrite(self):
        s = txf.Add(None, 'Added', (1,))
        self.assertRaises(txf.TransformException, txf.Copy, s, 'Added', 'Added')
