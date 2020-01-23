from bytecode import Compare


def adt_recog(cls):
    anns = getattr(cls, '__annotations__', {})
    n_field = len(anns)

    @staticmethod
    def __match__(i, val):
        if i is n_field and isinstance(val, cls):
            try:
                xs = []
                for each in cls.__annotations__:
                    xs.append(getattr(val, each))
                return tuple(xs)
            except AttributeError:
                return ()

    cls.__match__ = __match__
    return cls
