from .common import TransformException
from .split import Split
from .transform import Transform

import copy
import re

def bind_capture(name, pattern, outputs, defaults):

    regexp = re.compile(pattern)

    if regexp.groups != len(outputs):
        raise TransformException(f"Group count {regexp.groups} doesn't match the output count "
                                 f"{len(defaults)} in {name}")

    def capture(value):
        nonlocal regexp, outputs, defaults

        match = regexp.search(value)
        if match:
            return {output: match.group(i+1) or defaults[i] for i, output in enumerate(outputs)}

        result = {output: defaults[i] for i, output in enumerate(outputs)}
        result.update({outputs[0]: value})

        return result

    return capture

class Capture(Split):
    def __init__(self, source, input, outputs, pattern, defaults = ''):
        name = 'capture'
        outputs = Transform._validateStringTuple(name, outputs, 'Output')
        defaults = Transform._validateStringTuple(name, defaults, 'Default', len(outputs))
        separator = bind_capture(name, pattern, outputs, defaults)

        super().__init__(source, input, outputs, separator, defaults)

        self.name = name
        self.pattern = pattern

    def _schema(self):
        schema = super()._schema()

        #   The output types are all strings
        for output in self.outputs:
            Transform._updateSchemaType(schema, output, str)

        return schema

