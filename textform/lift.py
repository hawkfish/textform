from .common import TransformException
from .transform import Transform

import collections

class Lift(Transform):
    def __init__(self, source, input, default='', blank=''):
        super().__init__('lift', (input,), (), source)

        self.default = default
        self.blank = blank

        self._queue = collections.deque()
        self._lift = None

    def next(self):
        #   If the queue has rows, pull one out
        #   and copy the lifted value in
        if len(self._queue):
            row = self._queue.popleft()
            if row is not None:
                row[self.input] = self._lift
            return row

        #   Scan to the next lifted value
        self._lift = self.blank
        while self._lift == self.blank:
            row = super().next()
            self._queue.append(row)
            if row is None:
                self._lift = self.default
                break
            else:
                self._lift = row[self.input]

        #   Recurse once
        return self.next()

FillUp = Lift
