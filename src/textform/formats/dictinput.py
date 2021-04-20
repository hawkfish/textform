'''Base class for implementing csv.DictReader style interface'''

class NumberedIterator(object):

    def __init__(self, iterable, **config):
        self._iterable = iterable
        self.line_num = 0

    def __iter__(self):
        return self

    def __next__(self):
        values = next(self._iterable)
        self.line_num += 1
        return values

    next = __next__

class DictInput(object):

    def __init__(self, iterable, fieldnames=None, **config):
        self.reader = NumberedIterator(iterable)
        self.line_num = 0
        self._fieldnames = fieldnames
        self._defaultfieldnames = config.get('default_fieldnames')
        self._buffered = None

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                row = next(self.reader)
                self.line_num = self.reader.line_num
                if isinstance(row, dict):
                    #   If it is a dictionary, then hold onto it
                    self._fieldnames = tuple(row.keys())
                    self._buffered = row

                elif isinstance(row, (list, tuple,)):
                    self._fieldnames = tuple(row)

                else:
                    self._fieldnames = (row,)

            except StopIteration:
                #   Handle empty stream
                if self._fieldnames is None:
                    self._fieldnames = self._defaultfieldnames

        return self._fieldnames

    def __next__(self):
        if self.line_num == 0:
            self.fieldnames # Lazy instantiation

        values = next(self.reader) if self._buffered is None else self._buffered
        self._buffered = None
        self.line_num = self.reader.line_num

        result = {field: None for field in self.fieldnames}
        if isinstance(values, dict):
            result.update({field: values.get(field, None) for field in self.fieldnames})

        elif isinstance(values, (list, tuple,)):
            result.update(dict(zip(self.fieldnames, values)))

        else:
            result.update({field: values for field in self.fieldnames})

        return result

    next = __next__
