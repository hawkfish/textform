import unittest
from context import *

class TestLimit(unittest.TestCase):

    def assert_window(self, offset, limit):
        t = txf.Limit(None, limit, offset)

        self.assertEqual('limit', t.name)
        self.assertEqual(tuple(), t.inputs)
        self.assertEqual(tuple(), t.outputs)
        self.assertEqual(offset, t.offset)
        self.assertEqual(limit, t.limit)
        self.assertEqual(0, t._position)
        self.assertIsNone(t.source)

        self.assertEqual(t.schema, {})

        for row in t:
            self.assertEqual(row, {})
        self.assertRaises(StopIteration, t.readrow)
        self.assertEqual(offset + limit, t._position)

    def test_defaults(self):
        self.assert_window(0, 1)

    def test_limit(self):
        self.assert_window(0, 50)

    def test_offset(self):
        self.assert_window(50, 25)

    def test_invalid_offset(self):
        self.assertRaises(txf.TransformException, txf.Limit, None, 50, -1)

    def test_invalid_limit(self):
        self.assertRaises(txf.TransformException, txf.Limit, None, -50, 0)
