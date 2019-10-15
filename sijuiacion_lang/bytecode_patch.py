from bytecode import Instr
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
