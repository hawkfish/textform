import unittest
from context import *

class TestFold(unittest.TestCase):

    def assert_fold(self, nfolded=2, ngroups=1, nkeys=1, nrows=1):
        folded = tuple([f"Fold {f+1}" for f in range(nfolded*ngroups)])
        keys = [f"Key {k+1}" for k in range(nkeys)]
        inputs = [k for k in keys]
        inputs.extend(folded)

        values = [f"k{k}" for k in range(nkeys)]
        values.extend([f for f in range(nfolded*ngroups)])

        outputs = ['Tags',]
        outputs.extend([f'Group {g+1}' for g in range(ngroups)])

        rowid = 'Row'
        s = txf.Sequence(None, rowid)
        s = txf.Limit(s, nrows)
        s = txf.Add(s, inputs, values)
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
                self.assertFalse(input in t.schema)
                self.assertEqual(s.schema[input], t.schema[fold])

        actual = 0
        for row in t:
            #   Check the row id
            self.assertTrue(rowid in row)
            self.assertEqual(actual // nfolded, row[rowid])

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

        self.assertEqual(nfolded * nrows, actual)

        return t

    def test_fold_two_to_one(self):
        self.assert_fold()

    def test_fold_three_to_one(self):
        self.assert_fold(3)

    def test_fold_four_to_two(self):
        self.assert_fold(4, 2)

    def test_fold_four_to_two_twice(self):
        self.assert_fold(4, 2, 2)

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

    def test_voila_6(self):
        csv = ["#BLENDs,#Queries,Min,Q25,Median,Q75,Max",
            "5,1,7.22,7.22,7.22,7.22,7.22",
            "6,11,3.87,6.54,8.03,9.86,17.85",
            "7,85,5.18,7.20,8.16,10.14,311.77",
            "8,449,4.81,8.30,10.06,13.32,353.42",
            "9,1511,4.70,9.05,10.98,15.51,318.32",
            "10,9216,3.90,9.75,12.19,17.21,347.92",
        ]
        p = txf.Read(csv)
        p = txf.Cast(p, '#BLENDs', int)
        p = txf.Cast(p, '#Queries', int)
        unfolded = ['Min', 'Q25' ,'Median' ,'Q75' ,'Max',]
        folded = ['Quantile', 'Value',]
        p = txf.Fold(p, unfolded, folded)
        self.assertEqual(['#BLENDs','#Queries', ], p.fixed)
        actual = 0
        for row in p:
            self.assertTrue('#BLENDs' in row, row)
            self.assertEqual(5 + actual // len(unfolded), row['#BLENDs'], actual)
            actual += 1
        self.assertEqual((len(csv) - 1) * len(unfolded), actual)
