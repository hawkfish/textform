from .common import TransformException
from .transform import Transform

import csv

class Write(Transform):
    def __init__(self, source, outfile):
        if not source:
            raise TransformException(f"Can't write from missing input.")

        super().__init__('write', source.layout(), (), source)

        self._writer = csv.DictWriter(outfile, self.inputs())
        self._writer.writeheader()

    def next(self):
        row = super().next()
        if row is not None:
            self._writer.writerow(row)

        return row
