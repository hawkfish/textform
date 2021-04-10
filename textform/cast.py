from .common import TransformException
from .format import Format

def bind_cast(result_type):

    def cast(arg):
        if isinstance(arg, dict): return {'type': result_type}

        return result_type(arg)

    return cast

class Cast(Format):
    def __init__(self, source, input, result_type):
        super().__init__(source, input, bind_cast(result_type))

        self.name = 'cast'
        self.result_type = result_type
