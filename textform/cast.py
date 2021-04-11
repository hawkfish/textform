from .common import TransformException
from .format import Format

class Cast(Format):
    def __init__(self, source, input, result_type):
        super().__init__(source, input, result_type)

        self.name = 'cast'
        self.result_type = result_type

        #   We know the result type
        self.schema[self.input] = {'type': result_type}
        self._typed = True
