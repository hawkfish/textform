import unittest
from helpers import *

class TestFill(unittest.TestCase):

    def assert_fill(self, value, default, step=2, offset=0):
        input = 'Sparse'

        s = MockAlternate(input, value, step if step else 2 * offset + 1, offset)
        s = txf.Limit(s, offset + 100 * step)
        t = txf.Fill(s, input, default)

        self.assertEqual('fill', t.name, )
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)
        self.assertEqual(default, t.default)

        for r in range(0, offset):
            row = t.next()
            self.assertIsNotNone(row)
            self.assertTrue(input in row)
            self.assertEqual(default, row[input])

        for r in range(0, 100 * step):
            row = t.next()
            self.assertIsNotNone(row)
            self.assertTrue(input in row)
            self.assertEqual(value, row[input])

        self.assertIsNone(t.next())

        return t

    def test_fill_strings(self):
        value = 'String'
        default = 'Default'
        self.assert_fill(value, default)
        self.assert_fill(value, default, 10)
        self.assert_fill(value, default, 20, 10)
        self.assert_fill(value, default, 0, 500)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Fill, None, 'Target')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Fill, s, ('Target', 'Target',))
        self.assertRaises(txf.TransformException, txf.Fill, s, ())

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Fill, s, 'Missing')
