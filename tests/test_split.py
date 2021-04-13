import unittest
from context import *

class TestSplit(unittest.TestCase):

    def assert_split(self, sep, expecteds):
        input = 'Target'
        outputs = ('First', 'Second', 'Third', 'Fourth',)
        default = 'Default'

        s = txf.Sequence(None, input, 1000)
        s = txf.Limit(s, 100)
        s = txf.Cast(s, input, str)
        t = txf.Split(s, input, outputs, sep, default)

        self.assertEqual('split', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(sep, t.separator)
        self.assertEqual(tuple([default for o in outputs]), t.defaults)

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertIsNone(t.getSchemaType(output))
        self.assertFalse(input in t.schema)

        actuals = [0 for output in outputs]
        for row in t:
            for i, output in enumerate(outputs):
                if default == row[output]:
                    actuals[i] += 1

        self.assertEqual(expecteds, actuals)

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertEqual(s.schema[input], t.schema[output])
        self.assertFalse(input in t.schema)

        return t

    def test_split_none(self):
        self.assert_split(r'\s', [0, 100, 100, 100])

    def test_split_all(self):
        self.assert_split(r'1', [0, 0, 81, 99])

    def test_split_some(self):
        self.assert_split(r'5', [0, 81, 99, 100])

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Split, None, 'Target', ('First', 'Second',), r',')

    def test_missing(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Split, s, 'Missing', ('First', 'Second',), r',')

    def test_overwrite(self):
        s = txf.Add(None, ('Target', 'Bystander',), ('1234', 1234,))
        self.assertRaises(txf.TransformException, txf.Split, s, 'Target', ('First', 'Bystander',), r',')
        self.assertRaises(txf.TransformException, txf.Split, s, 'Target', ('Bystander', 'Second',), r',')

    def test_fill_count(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Split, s, 'Target', ('First', 'Second',), r',', ())
        self.assertRaises(txf.TransformException, txf.Split, s, 'Target', ('First', 'Second',), r',', ('',))
