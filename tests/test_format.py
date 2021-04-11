import unittest
from context import *

def square(arg):
    return arg * arg

class TestFormat(unittest.TestCase):

    def assert_format(self, value, function, expected):
        input = 'Target'
        s = txf.Add(None, input, value)
        t = txf.Format(s, input, function)

        self.assertEqual('format', t.name)
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(function, t.function)

        self.assertEqual({input: expected}, t.next())

        return t

    def test_format_date(self):
        self.assert_format(2, square, 4)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Format, None, 'Target', square)

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Format, s, ('Target', 'Target',), square)
        self.assertRaises(txf.TransformException, txf.Format, s, (), square)

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Format, s, 'Missing', square)
