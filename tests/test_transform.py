import unittest
from helpers import *

class TestTransform(unittest.TestCase):

    def test_defaults(self):
        t = txf.Transform('test')

        self.assertEqual(t.name, 'test')
        self.assertEqual(t.inputs, tuple())
        self.assertEqual(t.outputs, tuple())
        self.assertIsNone(t.source)

        self.assertEqual(t.schema, {})
        self.assertEqual(t.next(), {})

    def test_single_fields(self):
        t = txf.Transform('test', None, 'output')

        self.assertEqual(t.name, 'test')
        self.assertEqual(t.inputs, tuple())
        self.assertEqual(t.outputs, ('output',))
        self.assertIsNone(t.source)

        self.assertEqual(t.schema, {})
        self.assertEqual(t.next(), {})

    def test_source(self):
        s = MockSource('line')
        t = txf.Transform('test', 'line', 'output', s)

        self.assertEqual(t.name, 'test')
        self.assertEqual(t.inputs, ('line',))
        self.assertEqual(t.outputs, ('output',))
        self.assertEqual(t.source, s)

        self.assertEqual(t.schema, {'line': None})
        self.assertEqual(t.next(), {'line': None})

    def test_layout_replace_all(self):
        s = MockSource('line')
        t = txf.Transform('layout', 'line', 'output', s)

        self.assertEqual(['output',], t.layout)

    def test_layout_replace_first(self):
        s = MockSource(('F1', 'F2',))
        t = txf.Transform('layout', 'F1', 'R1', s)

        self.assertEqual(['R1', 'F2',], t.layout)

    def test_layout_replace_last(self):
        s = MockSource(('F1', 'F2',))
        t = txf.Transform('layout', 'F2', 'R2', s)

        self.assertEqual(['F1', 'R2',], t.layout)
