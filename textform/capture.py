from .common import TransformException
from .split import Split
from .transform import Transform

import copy
import re

def bind_capture(name, pattern, defaults):

    regexp = re.compile(pattern)

    if regexp.groups != len(defaults):
        raise TransformException(f"Group count {regexp.groups} doesn't match the output count "
        f"{len(defaults)} in {name}")

    def capture(value):
        nonlocal regexp, defaults

        if isinstance(value, dict): return [copy.copy(value) for default in defaults]

        match = regexp.search(value)
        if match:
            return match.groups(defaults[0])

        result = [value,]
        result.extend(defaults[1:])

        return result

    return capture

class Capture(Split):
    def __init__(self, source, input, outputs, pattern, defaults = ''):
        name = 'capture'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        separator = bind_capture(name, pattern, defaults)

        super().__init__(source, input, outputs, separator, defaults)

        self.name = name
        self.regexp = re.compile(pattern)
