import unittest
from context import *

def nullary():
    return 'Nullary'

def unary(*argv):
    if 'type' in argv[0]:
        return {'type': str}

    return argv[0]

class TestProject(unittest.TestCase):

    def assert_project(self, args, function, expected):
        inputs = ['Arg %d' % (i+1) for i in range(len(args))]
        output = 'Result'
        s = None
        if len(inputs): s = txf.Add(None, inputs, args)
        t = txf.Project(s, inputs, output, function)

        self.assertEqual('project', t.name)
        self.assertEqual(s, t.source)
        self.assertEqual(tuple(inputs), t.inputs)
        self.assertEqual((output,), t.outputs)

        self.assertEqual(output, t.output)
        self.assertEqual(function, t.function)

        layout = []
        layout.extend(inputs)
        layout.append(output)
        self.assertEqual(layout, t.layout)

        for input in inputs:
            self.assertTrue(input in t.schema)
            self.assertEqual(s.schema[input], t.schema[input])
        self.assertTrue(output in t.schema)
        self.assertIsNone(t.getSchemaType(output))

        row = t.next()
        self.assertIsNotNone(row)
        self.assertTrue(output in row)
        self.assertEqual(expected, row[output])

        for input in inputs:
            self.assertTrue(input in t.schema)
            self.assertEqual(s.schema[input], t.schema[input])
        self.assertTrue(output in t.schema)
        self.assertEqual(type(expected), t.getSchemaType(output))

        return t

    def test_project_nullary(self):
        self.assert_project((), nullary, 'Nullary')

    def test_project_unary(self):
        self.assert_project(('Unary',), unary, 'Unary')

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Project, None, ('F1',), 'Result', unary)

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Project, s, 'Missing', 'Result', unary)
