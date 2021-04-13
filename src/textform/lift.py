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
        self._stopped = None

    def readrow(self):
        #   If the queue has rows, pull one out
        #   and copy the lifted value in
        if len(self._queue):
            row = self._queue.popleft()
            row[self.input] = self._lift
            return row

        #   Are we finished?
        if self._stopped:
            raise self._stopped

        #   Scan to the readrow lifted value
        self._lift = self.blank
        while self._lift == self.blank:
            try:
                row = super().readrow()
                self._lift = row[self.input]
                self._queue.append(row)

            except StopIteration as stopped:
                self._lift = self.default
                self._stopped = stopped
                break

        #   Recurse once
        return self.readrow()

FillUp = Lift
