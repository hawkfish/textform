import unittest
from context import *

class TestDivide(unittest.TestCase):

    def assert_divide(self, pattern, expected):
        input = 'Target'
        left = 'Pass'
        right = 'Fail'

        s = txf.Sequence(None, input, 1000)
        s = txf.Limit(s, 100)
        s = txf.Cast(s, input, str)
        t = txf.Divide(s, input, left, right, pattern)

        self.assertEqual('divide', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((left, right,), t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(pattern, t.pattern)
        self.assertEqual(('', '',), t.fills)

        self.assertEqual(t.schema[left], t.schema[right])
        self.assertFalse(input in t.schema)
        self.assertEqual(s.schema[input], t.schema[right])

        actual = 0
        for row in t:
            if row[left]: actual += 1
        self.assertEqual(expected, actual)

        return t

    def test_divide_none(self):
        self.assert_divide(r'\s+', 0)

    def test_divide_all(self):
        self.assert_divide(r'\d+', 100)

    def test_divide_some(self):
        self.assert_divide(r'0$', 10)

    def test_divide_invert(self):
        self.assert_divide(r'[1-9]$', 90)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Divide, None, 'Target', 'Pass', 'Fail', r'\w+')

    def test_missing(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Divide, s, 'Missing', 'Pass', 'Fail', r'\w+')

    def test_overwrite(self):
        s = txf.Add(None, ('Target', 'Bystander',), ('1234', 1234,))
        self.assertRaises(txf.TransformException, txf.Divide, s, 'Target', 'Pass', 'Bystander', r'\w+')
        self.assertRaises(txf.TransformException, txf.Divide, s, 'Target', 'Bystander', 'Fail', r'\w+')

    def test_fill_count(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Divide, s, 'Target', 'Pass', 'Bystander', r'\w+', ())
        self.assertRaises(txf.TransformException, txf.Divide, s, 'Target', 'Pass', 'Bystander', r'\w+', ('',))
