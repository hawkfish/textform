from .common import TransformException
from .transform import Transform

class Unfold(Transform):
    def __init__(self, source, inputs, outputs):
        super().__init__('unfold', inputs, outputs, source)

        self._validateOutputs()

        self.tag = self.inputs[0]
        self.folds = self.inputs[1:]

        group_size = len(self.outputs) // len(self.folds)
        self._groups = [self.outputs[i:i+group_size] for i in range(0, len(self.outputs), group_size)]

        self.fixed = [f for f in filter(lambda input: input not in self.inputs, self.source.fieldnames)]

    def _schema(self):
        schema = super()._schema()

        folds = self.inputs[1:]
        if not len(folds):
            raise TransformException(f"Not enough inputs to {self.name} ({len(self.inputs)})")

        if len(self.outputs) % len(folds):
            raise TransformException(f"Ragged output count {len(self.outputs)} in {self.name}")

        group_size = len(self.outputs) // len(folds)
        if group_size < 1:
            raise TransformException(f"Not enough output columns to {self.name} ({group_size})")

        groups = [self.outputs[i:i+group_size] for i in range(0, len(self.outputs), group_size)]
        metadata = {groups[f][g]: schema[folds[f]] for f in range(len(folds)) for g in range(group_size)}

        for input in self.inputs:
            del schema[input]

        schema.update(metadata)

        return schema

    def readrow(self):
        #   Build the row, skipping a ragged end
        #   To do this in full generality would require
        #   buffering rows keyed by the fixed values
        #   and emitting a row whenever it is complete
        row = None
        for g in range(len(self._groups[0])):
            folded = super().readrow()

            if row is None: row = {fixed: folded[fixed] for fixed in self.fixed}
            row.update({self._groups[f][g]: folded[self.folds[f]] for f in range(len(self.folds))})

        self._updateSchemaTypes(row, self.outputs)

        return row
