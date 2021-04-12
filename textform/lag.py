from .common import TransformException
from .transform import Transform

import collections

class Lag(Transform):
    def __init__(self, source, input, lag=1, default=''):
        super().__init__('lag', (input,), (), source)

        self.lag = int(lag)
        self.default = default

        self._queue = collections.deque()
        if self.lag > 0:
            for i in range(self.lag):
                self._queue.append(self.default)

    def next(self):
        if self.lag > 0:
            #   Make sure the buffer is full of default values
            while len(self._queue) < self.lag:
                self._queue.append(self.default)

            row = super().next()
            if row is None:
                return row

            self._queue.append(row[self.input])
            row[self.input] = self._queue.popleft()

            return row

        elif self.lag < 0:
            #   Negative lags are leads
            lead = -self.lag

            #   Make sure the buffer is full of older rows
            while len(self._queue) < lead:
                self._queue.append(super().next())

            row = super().next()
            value = row[self.input] if row is not None else self.default
            self._queue.append(row)

            row = self._queue.popleft()
            if row is not None:
                row[self.input] = value

            return row

        else:
            #   Zero lags are a NOP
            return super().next()

class Lead(Lag):
    def __init__(self, source, input, lead=1, default=''):
        super().__init__(source, input, -lead, default)

        self.name = 'lead'
