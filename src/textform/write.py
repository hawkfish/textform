from .common import TransformException
from .layouts import DictWriterFactory
from .transform import Transform

class Write(Transform):
    def __init__(self, source, outfile, layout='csv', **params):
        super().__init__('write', source.fieldnames if source else (), (), source)

        self._requireSource()

        self._writer = DictWriterFactory(self.name, layout, outfile, self.fieldnames)
        self._writer.writeheader()

    def readrow(self):
        try:
            row = super().readrow()
            self._writer.writerow(row)
            return row

        except StopIteration:
            self._writer.writefooter()
            raise
