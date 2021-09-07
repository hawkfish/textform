from .split import Split
from .transform import Transform
from .common import TransformException
from .layouts import LineReaderFactory, BufferedAppender

def bind_iterate(name, layout, tag, **config):

    queue = BufferedAppender()
    reader = LineReaderFactory(name, layout, queue, **config)

    def iterate(value):
        nonlocal queue, reader, tag

        queue.append(value)

        row = next(reader)
        if isinstance(row, dict):
            return row

        elif isinstance(row, (list, tuple,)):
            return dict(zip(range(len(row)), row))

        else:
            return {tag: row}

    return iterate

class Iterate(Transform):
    def __init__(self, source, input, tags, strings, layout='csv', **config):
        super().__init__('iterate', input, (tags, strings,), source)

        self._validateOutputs(self.inputs)

        self.function = bind_iterate(self.name, layout, strings, **config)
        self._buffer = []
        self._position = len(self._buffer)

    def _schema(self):
        schema = super()._schema()
        for output in self.outputs:
            Transform._addSchemaType(schema, output, str)
        return schema

    def _unbuffer(self):
        if self._position < len(self._buffer):
            row = self._buffer[self._position]
            self._position += 1

            return row

        raise StopIteration(self.name)

    def readrow(self):
        if self._position < len(self._buffer):
            return self._unbuffer()

        #   Buffer flushed, so expand the next row
        row = self.source.readrow()
        ragged = self.function(row[self.input])
        del row[self.input]

        #   Update the buffer
        self._buffer = []
        for tag in ragged:
            buffered = dict(zip(self.outputs, (str(tag), str(ragged[tag]),)))
            buffered.update(row)
            self._buffer.append(buffered)

        self._position = 0

        #   Flush from refilled buffer
        return self._unbuffer()
