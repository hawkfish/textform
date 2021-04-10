import unittest
from helpers import *

class TestLift(unittest.TestCase):

    def assert_lift(self, value, default, step=2, offset=0):
        input = 'Sparse'
        limit = offset + 100 * step
        step = step if step else 2 * offset + 1

        s = MockAlternate(input, value, step, offset)
        s = txf.Limit(s, limit)
        t = txf.Lift(s, input, default)

        self.assertEqual('lift', t.name)
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(tuple(), t.outputs)
        self.assertEqual(default, t.default)

        #   The first non-blank is at (step - offset) % step
        #   All the other non-blanks are step away from that
        #   We will hit the defaults when the next non-blank
        #   is past limit.
        firstnonblank = (step - offset) % step
        nonblanks = (limit - firstnonblank - 1) // step
        lastnonblank = nonblanks * step + firstnonblank if nonblanks > 0 else -1
        for r in range(0, lastnonblank + 1):
            row = t.next()
            self.assertIsNotNone(row)
            self.assertTrue(input in row)
            self.assertEqual(value, row[input], r)

        for r in range(0, limit - lastnonblank - 1):
            row = t.next()
            self.assertIsNotNone(row)
            self.assertTrue(input in row)
            self.assertEqual(default, row[input], lastnonblank + 1 + r)

        self.assertIsNone(t.next())

        return t

    def test_lift_strings(self):
        value = 'String'
        default = 'Default'
        self.assert_lift(value, default)
        self.assert_lift(value, default, 10)
        self.assert_lift(value, default, 20, 10)
        self.assert_lift(value, default, 0, 500)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Lift, None, 'Target')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lift, s, ('Target', 'Target',))
        self.assertRaises(txf.TransformException, txf.Lift, s, ())

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lift, s, 'Missing')
