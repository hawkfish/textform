import unittest
from context import *

class TestFold(unittest.TestCase):

    def assert_fold(self, nfolded=2, ngroups=1, nkeys=1):
        folded = tuple([f"Fold {f+1}" for f in range(nfolded*ngroups)])
        keys = [f"Key {k+1}" for k in range(nkeys)]
        inputs = [k for k in keys]
        inputs.extend(folded)

        values = [f"k{k}" for k in range(nkeys)]
        values.extend([f for f in range(nfolded*ngroups)])

        outputs = ['Tags',]
        outputs.extend([f'Group {g+1}' for g in range(ngroups)])

        s = txf.Add(None, inputs, values)
        s = txf.Limit(s, 1)
        t = txf.Fold(s, folded, outputs)

        self.assertEqual('fold', t.name, )
        self.assertEqual(s, t.source)
        self.assertEqual(folded, t.inputs)
        self.assertEqual(tuple(outputs), t.outputs)

        self.assertEqual(outputs[0], t.tag)
        self.assertEqual(tuple(outputs[1:]), t.folds)

        self.assertTrue(t.tag in t.schema)
        self.assertEqual(str, t.getSchemaType(t.tag))
        for f, fold in enumerate(t.folds):
            self.assertTrue(fold in t.schema)
            for input in t.inputs[f*ngroups:(f+1)*ngroups]:
                self.assertEqual(s.schema[input], t.schema[fold])

        actual = 0
        while True:
            row = t.next()
            if row is None: break

            #   Check the keys
            for k, key in enumerate(keys):
                self.assertTrue(key in row)
                self.assertEqual(values[k], row[key])

            #   Check the tags
            rowno = actual % nfolded
            self.assertTrue(t.tag in row)
            self.assertEqual(t.tags[rowno], row[t.tag])

            #   Check folds
            for f, fold in enumerate(t.folds):
                self.assertTrue(fold in row)
                self.assertEqual(values[nkeys + f * nfolded + rowno], row[fold])

            actual += 1

        self.assertEqual(nfolded, actual)

        return t

    def test_fold_two_to_one(self):
        self.assert_fold()

    def test_fold_three_to_one(self):
        self.assert_fold(3)

    def test_fold_four_to_two(self):
        self.assert_fold(4, 2)

    def test_root(self):
        self.assertRaises(txf.TransformException, txf.Fold, None, ('F1', 'F2'), ('Tag', 'F',))

    def test_missing(self):
        s = txf.Add(None, 'Target', 1)
        self.assertRaises(txf.TransformException, txf.Fold, s, ('F1', 'F2'), ('Tag', 'F',))

    def assert_invalid(self, ninputs, noutputs, ntags=None):
        values = [i for i in range(ninputs)]
        inputs = [f"F{i}" for i in range(ninputs)]
        outputs = [f"O{i}" for i in range(noutputs)]
        tags = [f"T{i}" for i in range(ntags)] if ntags is not None else None

        s = txf.Add(None, inputs, values)
        self.assertRaises(txf.TransformException, txf.Fold, s, inputs, outputs, tags)

    def test_no_output(self):
        self.assert_invalid(2, 0)

    def test_only_tag(self):
        self.assert_invalid(2, 1)

    def test_not_enough_inputs(self):
        self.assert_invalid(1, 3)

    def test_ragged(self):
        self.assert_invalid(7, 4)

    def test_bad_tag_count(self):
        self.assert_invalid(4, 2, 3)
