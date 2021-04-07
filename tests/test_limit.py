import unittest
from context import *

def Construct(source=None, limit=1, offset=0):
    return txf.Limit(source, limit, offset)

class TestLimit(unittest.TestCase):

    def assert_window(self, offset, limit):
        t = Construct(None, limit, offset)

        self.assertEqual('limit', t.name(), )
        self.assertEqual(tuple(), t.inputs())
        self.assertEqual(tuple(), t.outputs())
        self.assertEqual(offset, t.offset(), )
        self.assertEqual(limit, t.limit(), )
        self.assertEqual(0, t.position(), )
        self.assertIsNone(t.source())

        self.assertEqual(t.schema(), {})

        for r in range(0,limit):
            self.assertEqual(t.next(), {})
        self.assertIsNone(t.next())
        self.assertEqual(offset + limit, t.position())

    def test_defaults(self):
        self.assert_window(0, 1)

    def test_limit(self):
        self.assert_window(0, 50)

    def test_offset(self):
        self.assert_window(50, 25)

    def test_invalid_offset(self):
        self.assertRaises(txf.TransformException, Construct, (None, 50, -1))

    def test_invalid_limit(self):
        self.assertRaises(txf.TransformException, Construct, (None, -50, 0))
