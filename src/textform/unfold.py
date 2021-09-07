from .common import TransformException
from .transform import Transform

class Unfold(Transform):
    def __init__(self, source, inputs, outputs):
        super().__init__('unfold', inputs, outputs, source)

        self._validateOutputs()

        self.tag = self.inputs[0]
        self.folds = tuple(self.inputs[1:])

        self._group_size = len(self.outputs) // len(self.folds)
        self._groups = tuple([self.outputs[i:i+self._group_size] for i in range(0, len(self.outputs), self._group_size)])

        self.fixed = tuple([f for f in filter(lambda input: input not in self.inputs, self.source.fieldnames)])

        # Ragged group buffer: {fixed: {tag: values}}
        self._buffer = {}

        # Map from tag values to group offsets
        self._tag_offsets = {}

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

    def _makeKey(self, row):
        return tuple([row[field] for field in self.fixed])

    def _poprow(self, fixed, key):
        row = {}
        row.update(fixed)
        row.update({output: None for output in self.outputs})

        # Map the group tags to the output fields
        tags = self._buffer.get(key, {})
        for tag, values in tags.items():
            tag_offset = self._tag_offsets[tag]
            row.update({self.outputs[tag_offset+i*self._group_size]: values[i] for i in range(len(values))})

        del self._buffer[key]

        self._updateSchemaTypes(row, self.outputs)

        return row

    def readrow(self):
        while True:
            folded = None
            try:
                folded = super().readrow()

            except StopIteration:
                if self._buffer:
                    key = next(iter(self._buffer))
                    fixed = {self.fixed[f]: key[f] for f in range(len(self.fixed))}
                    return self._poprow(fixed, key)
                raise

            # The buffer key is the fixed fields
            fixed = {fixed: folded[fixed] for fixed in self.fixed}

            # Record the tag mapping
            tag = folded[self.tag]
            if not tag in self._tag_offsets:
                self._tag_offsets[tag] = len(self._tag_offsets)
                if len(self._tag_offsets) > self._group_size:
                    raise TransformException("Too many fold tags in {self.name}")

            # Get the tags for this key
            key = self._makeKey(fixed)
            tags = self._buffer.get(key, {})
            if not tags: self._buffer[key] = tags

            values = tags.get(tag, [])
            if not values: tags[tag] = values
            values.extend([folded[fold] for fold in self.folds])

            if len(tags) == self._group_size:
                return self._poprow(fixed, key)
