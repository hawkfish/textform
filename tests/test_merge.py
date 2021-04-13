import unittest
from context import *

class TestMerge(unittest.TestCase):

    def assert_merge(self, values, glue=''):
        inputs = tuple(['F%d' % i for i in range(len(values))])
        output = 'Merged'

        s = txf.Add(None, inputs, values)
        t = txf.Merge(s, inputs, output, glue)

        self.assertEqual('merge', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual(inputs, t.inputs)
        self.assertEqual((output,), t.outputs)

        self.assertEqual(output, t.output)
        self.assertEqual(glue, t.glue)

        self.assertEqual(1, len(t.schema))
        self.assertTrue(output in t.schema)
        self.assertIsNone(t.getSchemaType(output))

        row = t.readrow()
        self.assertEqual(1, len(row))
        self.assertTrue(output in row)
        self.assertEqual(glue.join(values), row[output])

        self.assertEqual(1, len(t.schema))
        self.assertTrue(output in t.schema)
        self.assertEqual(type(row[output]), t.getSchemaType(output))

        return t

    def test_merge_left(self):
        self.assert_merge(('String', '',))

    def test_merge_right(self):
        self.assert_merge(('', 'String',))

    def test_merge_list(self):
        self.assert_merge(('1', '2', '3',), ',')

    def test_merge_one(self):
        self.assert_merge(('String',), ',')

    def test_merge_zero(self):
        self.assert_merge((), ',')

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Merge, None, ('F1', 'F2',), 'Merged')

    def test_missing(self):
        s = txf.Add(None, 'F1', '1234')
        self.assertRaises(txf.TransformException, txf.Merge, s, ('F1', 'F2',), 'Merged')

    def test_overwrite(self):
        s = txf.Add(None, ('F1', 'F2', 'Bystander',), ('String', '', 1234,))
        self.assertRaises(txf.TransformException, txf.Merge, s, ('F1','F2',), 'Bystander')
