import unittest
from context import *

class TestUnfold(unittest.TestCase):

    def assert_unfold(self, nfolded=2, ngroups=1, nkeys=1):
        keys = [f"Key {k+1}" for k in range(nkeys)]
        inputs = [k for k in keys]
        folded = ['Tags',]
        folded.extend([f"Group {g+1}" for g in range(ngroups)])
        inputs.extend(folded)

        values = [f"k{k}" for k in range(nkeys)]
        values.append('Tag')
        values.extend([g for g in range(ngroups)])

        outputs = [f'Fold {f+1}' for f in range(ngroups * nfolded)]

        s = txf.Add(None, inputs, values)
        s = txf.Limit(s, nfolded)
        t = txf.Unfold(s, folded, outputs)

        self.assertEqual('unfold', t.name, )
        self.assertEqual(s, t.source)
        self.assertEqual(tuple(folded), t.inputs)
        self.assertEqual(tuple(outputs), t.outputs)

        self.assertEqual(folded[0], t.tag)
        self.assertEqual(tuple(folded[1:]), t.folds)

        self.assertFalse(t.tag in t.schema)
        for f, fold in enumerate(t.folds):
            self.assertFalse(fold in t.schema)
            for output in t.outputs[f*ngroups:(f+1)*ngroups]:
                self.assertTrue(output in t.schema)
                self.assertEqual(s.schema[fold], t.schema[output])

        #   Only unfold a single row
        row = t.next()
        self.assertIsNotNone(row)

        #   Check the keys
        for k, key in enumerate(keys):
            self.assertTrue(key in row)
            self.assertEqual(values[k], row[key])

        #   Check unfolds
        group_size = len(t.outputs) // len(t.folds)
        for f, output in enumerate(t.outputs):
            self.assertTrue(output in row)
            self.assertEqual(values[nkeys + 1 + f // group_size], row[output], group_size)

        return t

    def test_unfold_two_to_one(self):
        self.assert_unfold()

    def test_unfold_three_to_one(self):
        self.assert_unfold(3)

    def test_unfold_four_to_two(self):
        self.assert_unfold(4, 2)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Unfold, None, ('F1', 'F2'), ('Tag', 'F',))

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Unfold, s, ('F1', 'F2'), ('Tag', 'F',))

    def assert_invalid(self, ninputs, noutputs, ntags=None):
        values = [i for i in range(ninputs)]
        inputs = [f"F{i}" for i in range(ninputs)]
        outputs = [f"O{i}" for i in range(noutputs)]

        s = txf.Add(None, inputs, values)
        self.assertRaises(txf.TransformException, txf.Unfold, s, inputs, outputs)

    def test_no_output(self):
        self.assert_invalid(2, 0)

    def test_only_tag(self):
        self.assert_invalid(1, 1)

    def test_not_enough_inputs(self):
        self.assert_invalid(1, 3)

    def test_ragged(self):
        self.assert_invalid(7, 4)

    def test_bad_tag_count(self):
        self.assert_invalid(4, 2, 3)
