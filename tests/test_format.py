import unittest
from context import *

class MockEmpty(txf.Transform):
    def next(self) : return None

class TestFormat(unittest.TestCase):

    def assert_format(self, value, search, replace, expected):
        input = 'Target'
        s = txf.Add(None, input, value)
        t = txf.Format(s, input, search, replace)

        self.assertEqual('format', t.name(), )
        self.assertIsNotNone(t.source())
        self.assertEqual((input,), t.inputs())
        self.assertEqual((), t.outputs())

        self.assertEqual({input: expected}, t.next())

        return t

    def test_format_dateg(self):
        self.assert_format('4/9/21', r'(\d+)/(\d+)/(\d+)', r'20\3-\1-\2', '2021-4-9')

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Format, None, 'Target', '', '')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Format, s, ('Target', 'Target',), '', '')
        self.assertRaises(txf.TransformException, txf.Format, s, (), '', '')

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Format, s, 'Missing', '', '')
