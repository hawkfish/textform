import unittest
from context import *

class TestMatch(unittest.TestCase):

    def assert_match(self, input, pattern, expected, invert=False):
        s = txf.Sequence(None, input, 1000)
        s = txf.Limit(s, 100)
        s = txf.Cast(s, input, str)
        t = txf.Match(s, input, pattern, invert)

        self.assertEqual('match', t.name, )
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(pattern, t.regexp.pattern)

        self.assertEqual(s.schema(), t.schema())

        actual = 0
        while t.next(): actual += 1
        self.assertEqual(expected, actual)
        return t

    def test_match_none(self):
        self.assert_match('Target', r'\s+', 0)

    def test_match_all(self):
        self.assert_match('Target', r'\d+', 100)

    def test_match_some(self):
        self.assert_match('Target', r'0$', 10)

    def test_match_invert(self):
        self.assert_match('Target', r'0$', 90, True)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Match, None, 'Target', r'\w+')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Match, s, ('Target', 'Target',), r'\w+')
        self.assertRaises(txf.TransformException, txf.Match, s, (), r'\w+')

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Match, s, 'Missing', r'\w+')
