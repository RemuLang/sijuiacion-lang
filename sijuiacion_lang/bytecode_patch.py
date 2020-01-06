from bytecode import Instr
from bytecode import concrete, instr
from marshal import dumps
import math

__all__ = ['IndirectJump']


class IndirectJump(Instr):
    def stack_effect(self, jump=None):
        return -2

    @property
    def name(self):
        return "END_FINALLY"

    @name.setter
    def name(self, v):
        pass

    def __repr__(self):
        return "<Indirect Jump>"


def const_key(obj):
    try:
        return dumps(obj)
    except ValueError:
        return id(obj), type(obj)


concrete.const_key = const_key
instr.const_key = const_key
