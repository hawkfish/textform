import unittest
from helpers import *

class TestCast(unittest.TestCase):

    def assert_cast(self, input, result_type, value):
        s = txf.Add(None, input, value)
        t = txf.Cast(s, input, result_type)

        self.assertEqual('cast', t.name, )
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)
        self.assertEqual(result_type, t.result_type)

        self.assertEqual(result_type, t.getSchemaType(input))
        self.assertEqual({input: result_type(value) }, t.next())

        return t

    def test_cast_string(self):
        self.assert_cast('Target', int, '10')

    def test_cast_int(self):
        self.assert_cast('Target', str, 10)

    def test_last_row(self):
        input = 'Added'
        t = txf.Add(MockEmpty('empty'), input, '10')
        t = txf.Cast(t, input, int)
        self.assertIsNone(t.next())

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Cast, None, 'Target', str)

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Cast, s, ('Target', 'Target',), str)
        self.assertRaises(txf.TransformException, txf.Cast, s, (), str)

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Cast, s, 'Missing', str)
