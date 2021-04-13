from .common import TransformException
from .transform import Transform

class Limit(Transform):
    def __init__(self, source=None, limit=1, offset=0):
        super().__init__('limit', (), (), source)

        if offset < 0: raise TransformException(f"Negative offset {offset} in {self.name}")
        self.offset = offset

        if limit < 0: raise TransformException(f"Negative limit {limit} in {self.name}")
        self.limit = limit

        self._position = 0

    def readrow(self):
        if self._position >= self.offset + self.limit:
            raise StopIteration(self.name)

        while self._position < self.offset:
            self._position += 1
            super().readrow()

        self._position += 1
        return super().readrow()
