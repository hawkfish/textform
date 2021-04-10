from .select import Select

import re

def bind_match(pattern, invert):

    regexp = re.compile(pattern)
    sense = not invert

    def predicate(arg):
        matched = True if regexp.search(arg) else False
        return matched == sense

    return predicate

class Match(Select):
    def __init__(self, source, input, pattern, invert=False):
        super().__init__(source, (input,), bind_match(pattern, invert))

        self.name = 'match'
        self.regexp = re.compile(pattern)
        self.invert = True if invert else False
