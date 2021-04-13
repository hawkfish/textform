import copy

from .common import TransformException

class Transform:
    def _validateTupleParameter(name, values, label, count=None):
        if values is None:
            values = tuple()

        elif isinstance(values, (list, tuple,)):
            values = tuple(values)

        elif count is None:
            values = (values,)

        else:
            values = tuple([values for i in range(count)])

        if count is not None and len(values) != count:
            raise TransformException(f"{label} count {len(values)} doesn't match the required count "
                                     f"{count} in {name}")

        return values

    def _validateTypedTuple(name, values, label, vtype, count=None):
        values = Transform._validateTupleParameter(name, values, label, count)

        for value in values:
            if not isinstance(value, vtype):
                raise TransformException(f"{label} '{value}' for {name} is not a {vtype.__name__}")

        return values

    def _validateStringTuple(name, strings, label, count=None):
        return Transform._validateTypedTuple(name, strings, label, str, count)

    def __init__(self, name, inputs=(), outputs=(), source=None):
        self.name = name

        self._setSource(source)
        self._setInputs(inputs)
        self._setOutputs(outputs)

        self._validateInputs()

        self.schema = self._schema()
        self._typed = self._isFullyTyped()

        self.fieldnames = self._fieldnames()

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

    def _validateOutputs(self, exceptions=()):
        schema = self.source.schema if self.source else {}
        for output in self.outputs:
            if output in schema and output not in exceptions:
                raise TransformException(f"Output field '{output}' in {self.name} overwrites an existing field.")
        return self.outputs

    def _fieldnames(self):
        fieldnames = copy.copy(self.source.fieldnames) if self.source else []

        #   Only update rows if there are outputs and inputs
        if len(self.outputs):
            #   Outputs are inserted at the first removed input
            leftmost = len(fieldnames)
            if self.inputs:
                leftmost = min([fieldnames.index(input) for input in self.inputs])
                fieldnames = list(filter(lambda input: input not in self.inputs, fieldnames))
            fieldnames[leftmost:leftmost] = list(self.outputs)

        return fieldnames

    def _getSchemaType(schema, field):
        return schema[field]['type']

    def getSchemaType(self, field):
        return Transform._getSchemaType(self.schema, field)

    def _updateSchemaType(schema, field, ftype = None):
        schema[field].update({'type': ftype})

    def updateSchemaType(self, field, ftype = None):
        Transform._updateSchemaType(self.schema, field, ftype)

    def _addSchemaType(schema, field, ftype = None):
        schema[field] = {'type': ftype}

    def _isFullyTyped(self):
        return sum(1 if self.getSchemaType(col) is None else 0 for col in self.schema) == 0

    def _updateSchemaTypes(self, row, fields):
        if not self._typed:
            for field in fields:
                self.updateSchemaType(field, type(row[field]))
            self._typed = self._isFullyTyped()

    def _schema(self):
        return copy.copy(self.source.schema) if self.source else {}

    def readrow(self):
        if self.source: return self.source.readrow()
        return {}

    def __iter__(self):
        return self

    def __next__(self):
        return self.readrow()

    next = __next__

    def pump(self):
        count = 0
        for row in self:
            count += 1

        return count
