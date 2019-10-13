from enum import Enum, auto as _auto
import abc
import typing as t
from dataclasses import dataclass


from sijuiacion_lang.compare import *


class Instr:
    pass


class UOp(Enum):
    POSITIVE = _auto()
    NEGATIVE = _auto()
    NOT = _auto()
    INVERT = _auto()
    pass


class BinOp(Enum):
    POWER = _auto()
    MULTIPLY = _auto()
    MATRIX_MULTIPLY = _auto()
    FLOOR_DIVIDE = _auto()
    TRUE_DIVIDE = _auto()
    MODULO = _auto()
    ADD = _auto()
    SUBTRACT = _auto()
    SUBSCR = _auto()
    LSHIFT = _auto()
    RSHIFT = _auto()
    AND = _auto()
    XOR = _auto()
    OR = _auto()
    pass


@dataclass(frozen=True, order=True)
class Load(Instr):
    name:str
    pass


@dataclass(frozen=True, order=True)
class Store(Instr):
    name:str
    pass


@dataclass(frozen=True, order=True)
class Global(Instr):
    name:str
    pass


@dataclass(frozen=True, order=True)
class Deref(Instr):
    name:str
    pass


@dataclass(frozen=True, order=True)
class RefSet(Instr):
    name:str
    pass


@dataclass(frozen=True, order=True)
class Const(Instr):
    val:object
    pass


@dataclass(frozen=True, order=True)
class Pop(Instr):
    pass


@dataclass(frozen=True, order=True)
class ROT(Instr):
    n:int
    pass


@dataclass(frozen=True, order=True)
class DUP(Instr):
    n:int
    pass


@dataclass(frozen=True, order=True)
class Goto(Instr):
    label_name:str
    pass


@dataclass(frozen=True, order=True)
class GotoEq(Instr):
    label_name:str
    pass


@dataclass(frozen=True, order=True)
class GotoNEq(Instr):
    label_name:str
    pass


@dataclass(frozen=True, order=True)
class Label(Instr):
    label_name:str
    pass


@dataclass(frozen=True, order=True)
class BlockAddr(Instr):
    label_name:str
    pass


@dataclass(frozen=True, order=True)
class Indir(Instr):
    pass


@dataclass(frozen=True, order=True)
class Bin(Instr):
    op:BinOp
    pass


@dataclass(frozen=True, order=True)
class IBin(Instr):
    op:BinOp
    pass


@dataclass(frozen=True, order=True)
class Un(Instr):
    op:UOp
    pass


@dataclass(frozen=True, order=True)
class Cmp(Instr):
    op:Compare
    pass


@dataclass(frozen=True, order=True)
class Attr(Instr):
    attr:str
    pass


@dataclass(frozen=True, order=True)
class AttrSet(Instr):
    attr:str
    pass


@dataclass(frozen=True, order=True)
class Item(Instr):
    pass


@dataclass(frozen=True, order=True)
class ItemSet(Instr):
    pass


@dataclass(frozen=True, order=True)
class PyCall(Instr):
    n:int
    pass


@dataclass(frozen=True, order=True)
class Call(Instr):
    n:int
    pass


@dataclass(frozen=True, order=True)
class Line(Instr):
    no:int
    pass


@dataclass(frozen=True, order=True)
class Defun(Instr):
    name:str
    args:t.List[str]
    suite:t.List[t.Union[Line,Instr]]
    pass


@dataclass(frozen=True, order=True)
class Mod:
    filename:str
    tops:t.List[Instr]
    pass
