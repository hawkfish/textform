import unittest
from context import *

import io

class TestRead(unittest.TestCase):

    def assert_read(self, text, outputs):
        output = 'Read'
        t = txf.Read(io.StringIO(text))

        self.assertEqual('read', t.name)
        self.assertIsNone(t.source)
        self.assertEqual(tuple(), t.inputs)
        self.assertEqual(outputs, t.outputs)

        self.assertEqual(list(outputs), t.layout)

        lines = len(text.split('\n')) - int(text[-1] == '\n') - 1 if text else 0
        self.assertEqual(lines, t.pull())

        for output in outputs:
            self.assertTrue(output in t.schema)
            self.assertEqual(str if lines else None, t.schema[output]['type'])

        return t

    def test_read_empty(self):
        self.assert_read('', ())

    def test_read_header(self):
        self.assert_read('Column\n', ('Column',))

    def test_read_missing_lf(self):
        read = 'Header\nValue'
        self.assert_read(read, ('Header',))

    def test_overwrite(self):
        text = io.StringIO('Overwrite\n')
        s = txf.Add(None, 'Overwrite', 1)
        self.assertRaises(txf.TransformException, txf.Read, text, s)
