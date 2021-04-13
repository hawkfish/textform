from .common import TransformException
from .transform import Transform

import re

class Project(Transform):
    def __init__(self, source, inputs, output, function):
        super().__init__('project', inputs, (output,), source)

        self.function = function

    def _fieldnames(self):
        #   Project doesn't drop the inputs
        fieldnames = self.source._fieldnames() if self.source else []
        #   Output is inserted after the last input
        rightmost = len(fieldnames)
        if len(self.inputs):
            rightmost = max([fieldnames.index(input) for input in self.inputs]) + 1
        fieldnames[rightmost:rightmost] = [self.output]

        return fieldnames

    def _schema(self):
        schema = super()._schema()
        Transform._addSchemaType(schema, self.output)
        return schema

    def readrow(self):
        row = super().readrow()

        #   Bind the input values
        argv = tuple([row[input] for input in self.inputs])
        row[self.output] = self.function(*argv)
        self._updateSchemaTypes(row, self.outputs)

        return row
