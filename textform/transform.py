from .common import TransformException

class Transform:
    def __init__(self, name, inputs=(), outputs=(), source=None):
        self._name = name

        if inputs is None:
            self._inputs = tuple()
        elif isinstance(inputs, str):
            self._inputs = (inputs,)
        else:
            self._inputs = tuple(inputs)
            for input in self._inputs:
                if not isinstance(input, str):
                    raise TransformException(f"Input for {self._name} is not a string")

        if outputs is None:
            self._outputs = tuple()
        elif isinstance(outputs, str):
            self._outputs = (outputs,)
        else:
            self._outputs = tuple(outputs)
            for output in self._outputs:
                if not isinstance(output, str):
                    raise TransformException(f"Output for {self._name} is not a string")

        if source and not isinstance(source, Transform):
            raise TransformException(f"Invalid source for {self._name}")
        self._source = source

        self._requireInputs()

    def _requireSource(self):
        if not self._source:
            raise TransformException(f"Can't {self._name} from missing input.")
        return self._source

    def _requireInputs(self):
        if self._source:
            schema = self._source.schema()
            for input in self._inputs:
                if input not in schema:
                    raise TransformException(f"Unknown input field '{input}' in {self._name}")

        elif len(self._inputs):
            raise TransformException(f"Unexpected input fields in {self._name}")

        return self._inputs

    def _requireOutputs(self, exceptions=()):
        schema = self._requireSource().schema() if self._source else {}
        for output in self._outputs:
            if output in schema and output not in  exceptions:
                raise TransformException(f"Output field '{output}' in {self._name} overwrites an existing field.")
        return self._outputs

    def name(self): return self._name
    def inputs(self): return self._inputs
    def outputs(self): return self._outputs
    def source(self): return self._source

    def layout(self):
        layout = self._source.layout() if self._source else []

        #   Only update rows if there are outputs and inputs
        if len(self._outputs):
            #   Outputs are inserted at the first removed input
            leftmost = len(layout)
            if self._inputs:
                leftmost = min([layout.index(input) for input in self._inputs])
                layout = list(filter(lambda input: input not in self._inputs, layout))
            layout[leftmost:leftmost] = list(self.outputs())

        return layout

    def schema(self):
        if self._source: return self._source.schema()
        return {}

    def next(self):
        if self._source: return self._source.next()
        return {}

    def pull(self):
        count = 0
        while True:
            row = self.next()
            if row is None: break
            count += 1

        return count
