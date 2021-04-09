import unittest
from context import *

class TestSequence(unittest.TestCase):

    def assert_sequence(self, output, start=0, step=1):
        t = txf.Sequence(None, output, start, step)

        self.assertEqual('sequence', t.name)
        self.assertEqual(tuple(), t.inputs)
        self.assertEqual((output,), t.outputs)
        self.assertEqual(start, t.start)
        self.assertEqual(step, t.step)
        self.assertEqual(start, t._position)
        self.assertIsNone(t.source)

        self.assertEqual(int, t.schema[output]['type'])

        if step:
            for expected in range(start, start+7*step, step):
                self.assertEqual({output: expected}, t.next())
        else:
            for i in range(0,7):
                self.assertEqual({output: start}, t.next())

    def test_defaults(self):
        self.assert_sequence('RowNum')

    def test_start(self):
        self.assert_sequence('RowNum', 50)
        self.assert_sequence('RowNum', -50)

    def test_step(self):
        self.assert_sequence('RowNum', 0, 5)
        self.assert_sequence('RowNum', 0, -5)
        self.assert_sequence('RowNum', 0, 0)

    def test_mixed(self):
        self.assert_sequence('RowNum', 10, 5)

    def test_input_count(self):
        self.assertRaises(txf.TransformException, txf.Sequence, None, ('Sequence 1', 'Sequence 2',))
        self.assertRaises(txf.TransformException, txf.Sequence, None, ())

    def test_overwrite(self):
        s = txf.Add(None, 'Sequence', 1)
        self.assertRaises(txf.TransformException, txf.Sequence, s, 'Sequence')
