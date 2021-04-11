from .common import TransformException, MakeLineWriter
from .transform import Transform

class Write(Transform):
    def __init__(self, source, outfile, format='csv', **params):
        super().__init__('write', source.layout if source else (), (), source)

        self._requireSource()

        self._writer = MakeLineWriter(self.name, format, outfile, self.layout)
        self._writer.writeheader()

    def next(self):
        row = super().next()
        if row is not None:
            self._writer.writerow(row)
        else:
            self._writer.writefooter()

        return row
