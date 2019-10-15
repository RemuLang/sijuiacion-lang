from bytecode import Compare
from dataclasses import astuple

def adt_recog(cls):
    anns = getattr(cls, '__annotations__', {})
    n_field = len(anns)
    @staticmethod
    def __match__(i, val):
        if i is n_field and isinstance(val, cls):
            return astuple(val)
    cls.__match__ = __match__
    return cls
