import unittest
from context import *

import io

class TestUnnest(unittest.TestCase):

    def assert_unnest(self, lines):
        input = 'Line'
        outputs = ('Row#', 'String',)
        text = '\n'.join([f'{i},"String {i}"' for i in range(lines)])
        s = txf.Text(io.StringIO(text), input)
        t = txf.Unnest(s, input, outputs)

        self.assertEqual('unnest', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual((input,), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(input, t.input)

        self.assertEqual(list(outputs), t.layout)

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertEqual(str, t.schema[output]['type'])

        self.assertEqual(lines, t.pull())

        return t

    def test_unnest_zero(self):
        self.assert_unnest(0)

    def test_unnest_one(self):
        self.assert_unnest(1)

    def test_unnest_two(self):
        self.assert_unnest(2)

    def test_unnest_ten(self):
        self.assert_unnest(10)

    def test_overwrite(self):
        text = io.StringIO('Col 1,Col 2\n')
        s = txf.Add(None, ('Target', 'Overwrite',), ('String', 1,))
        self.assertRaises(txf.TransformException, txf.Unnest, s, 'Target', ('First', 'Overwrite',))
