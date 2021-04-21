import unittest
from context import *

import io

class MockFormat(object):

    def LineReader(iterable, **config):
        pass

    def DictReader(iterable, fieldnames, **config):
        pass

    def LineWriter(outfile, fieldnames, **config):
        pass

    def DictWriter(outfile, fieldnames, **config):
        pass

class TestRegisterLayout(unittest.TestCase):

    def test_get_layout(self):
        actual = txf.layouts.GetLayout('csv')
        self.assertEqual(4, len(actual))

    def test_register_layout(self):
        name = 'test'
        layout = 'mock'
        lines = ['Line 1', 'Line 2']
        fieldnames = ('Text',)
        config = {'param': 'value'}
        outfile = io.StringIO()

        try:
            txf.layouts.RegisterLayout(layout, MockFormat)
            txf.layouts.LineReaderFactory(name, layout, iter(lines), **config)
            txf.layouts.DictReaderFactory(name, layout, iter(lines), fieldnames, **config)
            txf.layouts.LineWriterFactory(name, layout, outfile, fieldnames, **config)
            txf.layouts.DictWriterFactory(name, layout, outfile, fieldnames, **config)
        finally:
            txf.layouts.UnregisterLayout(layout)
