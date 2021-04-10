import copy

from .common import TransformException

class Transform:
    def _validateStringTuple(name, strings, label, count=None):
        if strings is None:
            strings = tuple()

        elif isinstance(strings, str):
            if count is None:
                strings = (strings,)
            else:
                strings = tuple([strings for i in range(count)])

        else:
            strings = tuple(strings)
            for string in strings:
                if not isinstance(string, str):
                    raise TransformException(f"{label} '{string}' for {name} is not a string")

        if count is not None and len(strings) != count:
            raise TransformException(f"{label} count {len(strings)} doesn't match the required count "
            f"{count} in {name}")

        return strings

    def __init__(self, name, inputs=(), outputs=(), source=None):
        self.name = name

        self._setSource(source)
        self._setInputs(inputs)
        self._setOutputs(outputs)

        self._validateInputs()

        self.schema = self._schema()
        self.layout = self._layout()

    def _setSource(self, source):
        if source and not isinstance(source, Transform):
            raise TransformException(f"Invalid source for {self.name}")
        self.source = source

    def _setInputs(self, inputs):
        self.inputs = Transform._validateStringTuple(self.name, inputs, 'Input')
        if len(self.inputs) == 1: self.input = self.inputs[0]

    def _setOutputs(self, outputs):
        self.outputs = Transform._validateStringTuple(self.name, outputs, 'Output')
        if len(self.outputs) == 1: self.output = self.outputs[0]

    def _requireSource(self):
        if not self.source:
            raise TransformException(f"Can't {self.name} from missing input.")
        return self.source

    def _validateInputs(self):
        if self.source:
            schema = self.source.schema
            for input in self.inputs:
                if input not in schema:
                    raise TransformException(f"Unknown input field '{input}' in {self.name}")

        elif len(self.inputs):
            raise TransformException(f"Unexpected input fields in {self.name}")

        return self.inputs

    def _requireOutputs(self, exceptions=()):
        schema = self._requireSource().schema if self.source else {}
        for output in self.outputs:
            if output in schema and output not in exceptions:
                raise TransformException(f"Output field '{output}' in {self.name} overwrites an existing field.")
        return self.outputs

    def _layout(self):
        layout = copy.copy(self.source.layout) if self.source else []

        #   Only update rows if there are outputs and inputs
        if len(self.outputs):
            #   Outputs are inserted at the first removed input
            leftmost = len(layout)
            if self.inputs:
                leftmost = min([layout.index(input) for input in self.inputs])
                layout = list(filter(lambda input: input not in self.inputs, layout))
            layout[leftmost:leftmost] = list(self.outputs)

        return layout

    def _schema(self):
        return copy.copy(self.source.schema) if self.source else {}

    def next(self):
        if self.source: return self.source.next()
        return {}

    def pull(self):
        count = 0
        while True:
            row = self.next()
            if row is None: break
            count += 1

        return count
