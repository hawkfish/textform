import unittest
from context import *

import io

class TestText(unittest.TestCase):

    def assert_text(self, text):
        output = 'Text'
        t = txf.Text(io.StringIO(text), output)

        self.assertEqual('text', t.name)
        self.assertIsNone(t.source)
        self.assertEqual(tuple(), t.inputs)

        self.assertEqual(output, t.output)

        self.assertTrue(output in t.schema)
        self.assertEqual(str, t.getSchemaType(output))

        expected = len(text.split('\n')) - int(text[-1] == '\n') if text else 0
        self.assertEqual(expected, t.pull())

        return t

    def assert_lines(self, count):
        text = '\n'.join(['Line %d' % (i + 1) for i in range(count)])
        self.assert_text(text)

    def test_text_empty(self):
        self.assert_text('')

    def test_text_multiple(self):
        for count in range(10):
            self.assert_lines(count)

    def test_text_missing_lf(self):
        text = 'Line 1\nLine2'
        self.assert_text(text)

    def test_overwrite(self):
        s = txf.Add(None, 'Overwrite', 1)
        self.assertRaises(txf.TransformException, txf.Text, '', 'Overwrite', s)
