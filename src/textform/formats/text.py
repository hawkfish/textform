class Reader(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self._iterable = iterable

        self.fieldnames = fieldnames
        if not self.fieldnames:
            self.fieldnames = tuple(config.get('default_fieldnames', ()))
        self.fieldnames = self.fieldnames[:1]

    def __iter__(self):
        return self;

    def __next__(self):
        return {self.fieldnames[0]: next(self._iterable)}

    next = __next__

Unnester = Reader
