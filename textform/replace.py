from .common import TransformException
from .format import Format

import copy
import re

def bind_replace(pattern, expansion):

    search = re.compile(pattern)

    def replace(arg):
        match = search.search(arg)
        if match:
            return match.expand(expansion)
        else:
            return arg

    return replace

class Replace(Format):
    def __init__(self, source, input, pattern, replace):
        super().__init__(source, input, bind_replace(pattern, replace))

        self.name = 'replace'
        self.search = re.compile(pattern)
        self.replace = replace

        #   We know the type
        self.schema[self.input] = copy.copy(self.source.schema[self.input])
        self._typed = True
