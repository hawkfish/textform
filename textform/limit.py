from .common import TransformException
from .transform import Transform

class Limit(Transform):
    def __init__(self, source=None, limit=1, offset=0):
        super().__init__('limit', (), (), source)

        if offset < 0: raise TransformException(f"Negative offset {offset} in {self.name()}")
        self._offset = offset

        if limit < 0: raise TransformException(f"Negative limit {limit} in {self.name()}")
        self._limit = limit

        self._position = 0

    def offset(self): return self._offset
    def limit(self): return self._limit
    def position(self): return self._position

    def next(self):
        if self._position >= self._offset + self._limit:
            return None

        while self._position < self._offset:
            self._position += 1
            super().next()

        self._position += 1
        return super().next()
