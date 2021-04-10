import unittest
from context import *

class TestCapture(unittest.TestCase):

    def assert_capture(self, pattern, expected):
        input = 'Target'
        outputs = ('First', 'Second',)

        s = txf.Sequence(None, input, 1000)
        s = txf.Limit(s, 100)
        s = txf.Cast(s, input, str)
        t = txf.Capture(s, input, outputs, pattern)

        self.assertEqual('capture', t.name, )
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)
        self.assertEqual(pattern, t.pattern)

        schema = t.schema
        self.assertFalse(input in schema)
        for output in outputs:
            self.assertEqual(schema[outputs[0]], schema[output])

        actual = 0
        while True:
            row = t.next()
            if row is None: break
            if row[outputs[1]]: actual += 1
        self.assertEqual(expected, actual)

        return t

    def test_capture_none(self):
        self.assert_capture(r'(\s+)(\w+)', 0)

    def test_capture_all(self):
        self.assert_capture(r'(\d)(\d+)', 100)

    def test_capture_some(self):
        self.assert_capture(r'(\d+)(0)$', 10)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Capture, None, 'Target', ('First', 'Second',), r'\w+')

    def test_missing(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Capture, s, 'Missing', ('First', 'Second',), r'\w+')

    def test_overwrite(self):
        s = txf.Add(None, ('Target', 'Bystander',), ('1234', 1234,))
        self.assertRaises(txf.TransformException, txf.Capture, s, 'Target', ('First', 'Bystander',), r'\w+')
        self.assertRaises(txf.TransformException, txf.Capture, s, 'Target', ('Bystander', 'Second',), r'\w+')

    def test_group_count(self):
        s = txf.Add(None, 'Target', '1234')
        self.assertRaises(txf.TransformException, txf.Capture, s, 'Target', ('First', 'Second',), r'(\w+)')
        self.assertRaises(txf.TransformException, txf.Capture, s, 'Target', ('First', 'Second',), r'(\w+) (\w+) (\w+)')
