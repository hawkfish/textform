import unittest
from context import *

class TestReplace(unittest.TestCase):

    def assert_replace(self, value, pattern, replace, expected):
        input = 'Target'
        s = txf.Add(None, input, value)
        t = txf.Replace(s, input, pattern, replace)

        self.assertEqual('replace', t.name)
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(pattern, t.search.pattern)
        self.assertEqual(replace, t.replace)

        self.assertEqual(type(expected), t.getSchemaType(input))

        self.assertEqual({input: expected}, t.next())

        return t

    def test_replace_date(self):
        self.assert_replace('4/9/21', r'(\d+)/(\d+)/(\d+)', r'20\3-\1-\2', '2021-4-9')

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Replace, None, 'Target', '', '')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Replace, s, ('Target', 'Target',), '', '')
        self.assertRaises(txf.TransformException, txf.Replace, s, (), '', '')

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Replace, s, 'Missing', '', '')
