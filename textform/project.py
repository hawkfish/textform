from .common import TransformException
from .transform import Transform

import re

class Project(Transform):
    def __init__(self, source, inputs, output, function):
        super().__init__('project', inputs, (output,), source)

        if len(inputs): self._requireSource()

        self._function = function

    def function(self): return self._function

    def output(self): return self._outputs[0]

    def layout(self):
        #   Project doesn't drop the inputs
        layout = self._source.layout()
        #   Output is inserted after the last input
        rightmost = len(layout)
        if len(self._inputs):
            rightmost = max([layout.index(input) for input in self._inputs]) + 1
        layout[rightmost:rightmost] = self.output()

        return layout

    def schema(self):
        schema = super().schema()
        argv = tuple([schema[input] for input in self._inputs])
        metadata = self._function(*argv)
        #   Hack for nullary arguments
        if len(argv) == 0: metadata = {'type': type(metadata)}
        schema[self.output()] = metadata
        return schema

    def next(self):
        while True:
            row = super().next()
            if row is None: break

            #   Bind the input values
            argv = tuple([row[input] for input in self._inputs])
            row[self.output()] = self._function(*argv)

            return row

        return None
