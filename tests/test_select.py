import unittest
from context import *

def predicate_false(rowno):
    return False

def predicate_true(rowno):
    return True

def predicate_even(rowno):
    return rowno % 2 != 0

def predicate_odd(rowno):
    return rowno % 2

class TestSelect(unittest.TestCase):

    def assert_select(self, input, predicate, expected):
        s = txf.Sequence(None, input, 1000)
        s = txf.Limit(s, 100)
        t = txf.Select(s, input, predicate)

        self.assertEqual('select', t.name(), )
        self.assertEqual(s, t.source())
        self.assertEqual((input,), t.inputs())
        self.assertEqual((), t.outputs())

        self.assertEqual(predicate, t.predicate())

        self.assertEqual(s.schema(), t.schema())

        actual = t.pull()
        self.assertEqual(expected, actual)

        return t

    def test_select_none(self):
        self.assert_select('rowno', predicate_false, 0)

    def test_select_all(self):
        self.assert_select('rowno', predicate_true, 100)

    def test_select_even(self):
        self.assert_select('rowno', predicate_even, 50)

    def test_select_odd(self):
        self.assert_select('rowno', predicate_odd, 50)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Select, None, 'Arg', predicate_false)

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Select, s, 'Missing', predicate_false)
