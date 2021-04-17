from .common import TransformException
from .split import Split
from .transform import Transform

import copy
import re

def bind_capture(name, pattern, outputs):

    regexp = re.compile(pattern)

    if regexp.groups != len(outputs):
        raise TransformException(f"Group count {regexp.groups} doesn't match the output count "
                                 f"{len(outputs)} in {name}")

    def capture(value):
        nonlocal regexp, outputs

        match = regexp.search(value)
        if match:
            return match.groups()

        return [value,]

    return capture

class Capture(Split):
    def __init__(self, source, input, outputs, pattern, defaults = ''):
        name = 'capture'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        separator = bind_capture(name, pattern, outputs)

        super().__init__(source, input, outputs, separator, defaults)

        self.name = name
        self.pattern = pattern

    def _schema(self):
        schema = super()._schema()

        #   The output types are all strings
        for output in self.outputs:
            Transform._updateSchemaType(schema, output, str)

        return schema

