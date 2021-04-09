from .common import TransformException
from .transform import Transform

import re

class Project(Transform):
    def __init__(self, source, inputs, output, function):
        super().__init__('project', inputs, (output,), source)

        self.function = function

    def layout(self):
        #   Project doesn't drop the inputs
        layout = self.source.layout() if self.source else []
        #   Output is inserted after the last input
        rightmost = len(layout)
        if len(self.inputs):
            rightmost = max([layout.index(input) for input in self.inputs]) + 1
        layout[rightmost:rightmost] = [self.output]

        return layout

    def schema(self):
        schema = super().schema()
        argv = tuple([schema[input] for input in self.inputs])
        metadata = self.function(*argv)
        #   Hack for nullary arguments
        if len(argv) == 0: metadata = {'type': type(metadata)}
        schema[self.output] = metadata
        return schema

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            #   Bind the input values
            argv = tuple([row[input] for input in self.inputs])
            row[self.output] = self.function(*argv)

            return row

        return None
