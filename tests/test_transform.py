import unittest
from context import *

class MockSource(Transform):
    def __init__(self, outputs):
        super().__init__('source', (), outputs)

    def schema(self):
        return {output: None for output in self._outputs}

    def next(self):
        return {output: None for output in self._outputs}

class TestTransform(unittest.TestCase):

    def test_defaults(self):
        t = Transform('test')

        self.assertEqual(t.name(), 'test')
        self.assertEqual(t.inputs(), tuple())
        self.assertEqual(t.outputs(), tuple())
        self.assertIsNone(t.source())

        self.assertEqual(t.schema(), {})
        self.assertEqual(t.next(), {})

    def test_single_fields(self):
        t = Transform('test', None, 'output')

        self.assertEqual(t.name(), 'test')
        self.assertEqual(t.inputs(), tuple())
        self.assertEqual(t.outputs(), ('output',))
        self.assertIsNone(t.source())

        self.assertEqual(t.schema(), {})
        self.assertEqual(t.next(), {})

    def test_source(self):
        s = MockSource('line')
        t = Transform('test', 'line', 'output', s)

        self.assertEqual(t.name(), 'test')
        self.assertEqual(t.inputs(), ('line',))
        self.assertEqual(t.outputs(), ('output',))
        self.assertEqual(t.source(), s)

        self.assertEqual(t.schema(), {'line': None})
        self.assertEqual(t.next(), {'line': None})
