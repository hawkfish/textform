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

        if outputs is None:
            self._outputs = tuple()
        elif isinstance(outputs, str):
            self._outputs = (outputs,)
        else:
            self._outputs = tuple(outputs)

        if source and not isinstance(source, Transform):
            raise TransformException(f"Invalid source for {name} transform")
        self._source = source

        #   Smoke check the schema
        if self._source:
            schema = self._source.schema()
            for field in self._inputs:
                if field not in schema:
                    raise TransformException(f"Unknown input field '{field}' in {name} transform")
        elif len(self._inputs):
            raise TransformException(f"Extra input fields in {name} transform")

    def name(self): return self._name
    def inputs(self): return self._inputs
    def outputs(self): return self._outputs
    def source(self): return self._source

    def schema(self):
        if self._source: return self._source.schema()
        return {}

    def next(self):
        if self._source: return self._source.next()
        return {}
