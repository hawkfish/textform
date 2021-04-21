#   deque doesn't like to be modified while iterating
class BufferedAppender(object):

    def __init__(self):
        self.buffer = None
        self.buffered = False

    def __iter__(self):
        return self

    def append(self, value):
        self.buffer = value
        self.buffered = True

    def __next__(self):
        if not self.buffered:
            raise StopIteration("BufferedIterator")

        result = self.buffer
        self.buffered = False
        return result

    next = __next__

class BufferedWriter(object):

    def __init__(self):
        self.buffer = None
        self.buffered = False

    def __iter__(self):
        return self

    def write(self, value):
        if not self.buffered:
            self.buffer = value
            self.buffered = True
        else:
            self.buffer += value

    def __next__(self):
        if not self.buffered:
            raise StopIteration("BufferedWriter")

        result = self.buffer
        self.buffered = False

        return result

    next = __next__
