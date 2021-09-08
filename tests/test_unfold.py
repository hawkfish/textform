import unittest
from context import *

class TestUnfold(unittest.TestCase):

    def assert_unfold(self, nfolded=2, ngroups=1, nkeys=1):
        keys = [f"Key {k+1}" for k in range(nkeys)]
        inputs = [k for k in keys]
        groups = [f"Group {g+1}" for g in range(ngroups)]
        folded = ['Tags',]
        folded.extend(groups)
        inputs.extend(folded)

        values = [f"k{k+1}" for k in range(nkeys)]
        values.append('Tag')
        values.extend([g for g in range(ngroups)])

        outputs = [f'Fold {f+1}' for f in range(ngroups * nfolded)]

        s = txf.Sequence(None, 'RowID', 0)
        s = txf.Limit(s, nfolded)
        s = txf.Add(s, keys, values[:nkeys])
        s = txf.Project(s, ('RowID',), 'Tags', lambda r: r % nfolded)
        s = txf.Add(s, groups, values[nkeys+1:])
        s = txf.Drop(s, 'RowID')
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
        row = t.readrow()

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

    def test_voila_6(self):
        csv = ["#BLENDs,#Queries,Quantile,Value",
            "5,1,Min,7.22",
            "5,1,Q25,7.22",
            "5,1,Median,7.22",
            "5,1,Q75,7.22",
            "5,1,Max,7.22",
            "6,11,Min,3.87",
            "6,11,Q25,6.54",
            "6,11,Median,8.03",
            "6,11,Q75,9.86",
            "6,11,Max,17.85",
            "7,85,Min,5.18",
            "7,85,Q25,7.20",
            "7,85,Median,8.16",
            "7,85,Q75,10.14",
            "7,85,Max,311.77",
            "8,449,Min,4.81",
            "8,449,Q25,8.30",
            "8,449,Median,10.06",
            "8,449,Q75,13.32",
            "8,449,Max,353.42",
            "9,1511,Min,4.70",
            "9,1511,Q25,9.05",
            "9,1511,Median,10.98",
            "9,1511,Q75,15.51",
            "9,1511,Max,318.32",
            "10,9216,Min,3.90",
            "10,9216,Q25,9.75",
            "10,9216,Median,12.19",
            "10,9216,Q75,17.21",
            "10,9216,Max,347.92",
        ]

        p = txf.Read(csv)
        p = txf.Cast(p, '#BLENDs', int)
        p = txf.Cast(p, '#Queries', int)
        p = txf.Cast(p, 'Value', float)
        unfolded = ['Min', 'Q25' ,'Median' ,'Q75' ,'Max',]
        folded = ['Quantile', 'Value',]
        offsets = {f: i for (i,f) in enumerate(unfolded)}
        p = txf.Unfold(p, folded, unfolded, offsets)
        self.assertEqual(('#BLENDs','#Queries',), p.fixed)
        actual = 0
        for row in p:
            self.assertTrue('#BLENDs' in row, row)
            self.assertEqual(5 + actual, row['#BLENDs'], actual)
            actual += 1
        self.assertEqual((len(csv) - 1) // len(unfolded), actual)
