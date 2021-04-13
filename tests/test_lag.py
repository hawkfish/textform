import unittest
from context import *

class TestLag(unittest.TestCase):

    def assert_lag(self, lag=1):
        input = 'Row'
        default = -1
        limit = 10 * abs(lag)

        s = txf.Sequence(None, input)
        s = txf.Limit(s, limit)
        t = txf.Lag(s, input, lag, default)

        self.assertEqual('lag', t.name)
        self.assertIsNotNone(t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual((), t.outputs)
        self.assertEqual(lag, t.lag)
        self.assertEqual(default, t.default)

        self.assertTrue(input in t.schema)
        self.assertEqual(int, t.getSchemaType(input))

        if lag >= 0:
            for r in range(lag):
                row = t.readrow()
                self.assertTrue(input in row)
                self.assertEqual(default, row[input])

            for r in range(lag, limit):
                row = t.readrow()
                self.assertTrue(input in row)
                self.assertEqual(r - lag, row[input])

        else:
            for r in range(0, limit+lag):
                row = t.readrow()
                self.assertTrue(input in row)
                self.assertEqual(r - lag, row[input])

            for r in range(-lag):
                row = t.readrow()
                self.assertTrue(input in row)
                self.assertEqual(default, row[input])

        self.assertRaises(StopIteration, t.readrow)

        return t

    def test_lag(self):
        self.assert_lag(0)
        self.assert_lag(1)
        self.assert_lag(2)
        self.assert_lag(5)

    def test_lead(self):
        self.assert_lag(-1)
        self.assert_lag(-2)
        self.assert_lag(-5)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Lag, None, 'Target')

    def test_input_count(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lag, s, ('Target', 'Target',))
        self.assertRaises(txf.TransformException, txf.Lag, s, ())

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Lag, s, 'Missing')
