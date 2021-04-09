from .common import TransformException
from .transform import Transform

class Fold(Transform):
    def __init__(self, source, inputs, outputs, tags=None):
        super().__init__('fold', inputs, outputs, source)

        self.tag = self.outputs[0]
        self.folds = self.outputs[1:]

        group_size = len(self.inputs) // len(self.folds)
        self._groups = [self.inputs[i:i+group_size] for i in range(0, len(self.inputs), group_size)]

        if tags is None:
            self.tags = tuple([','.join([group[g] for group in self._groups]) for g in range(group_size)])
        elif isinstance(tags, (list, tuple,)):
            self.tags = tuple(tags)
        else:
            raise TransformException(f"Invalid tags in {self.name}")

        if group_size != len(self.tags):
            raise TransformException(f"Wrong number of tags ({len(self.tags)}) in {self.name}")

        self._buffer = [{self.tag: tag} for tag in self.tags]
        self._position = len(self._buffer)

        self._fixed = filter(lambda input: input not in self.inputs, self.source.layout)

    def _schema(self):
        schema = super()._schema()

        folds = self.outputs[1:]
        if not len(folds):
            raise TransformException(f"Not enough outputs to {self.name} ({len(self.outputs)})")

        if len(self.inputs) % len(folds):
            raise TransformException(f"Ragged input count {len(self.inputs)} in {self.name}")

        group_size = len(self.inputs) // len(folds)
        if group_size < 1:
            raise TransformException(f"Not enough columns to {self.name} ({len(group_size)})")

        groups = [self.inputs[i:i+group_size] for i in range(0, len(self.inputs), group_size)]
        metadata = {folds[g]: schema[group[0]] for g, group in enumerate(groups)}
        metadata[self.outputs[0]] = {'type': str}

        for input in self.inputs:
            del schema[input]

        schema.update(metadata)

        return schema

    def _buffered(self):
        if self._position < len(self._buffer):
            row = self._buffer[self._position]
            self._position += 1
            return row
        return None

    def next(self):
        row = self._buffered()
        if row is not None: return row

        #   Buffer empty, so pivot next row
        row = super().next()
        if row is not None:
            #   Update the folds
            for g, group in enumerate(self._groups):
                pivot = self.outputs[g+1]
                for b, buffered in enumerate(self._buffer):
                    buffered[pivot] = row[group[b]]

            #   Update the fixed values
            fixed = {f: row[f] for f in self._fixed}
            for buffered in self._buffer:
                buffered.update(fixed)

            self._position = 0

            #   Flush from refilled buffer
            return self._buffered()

        return row
