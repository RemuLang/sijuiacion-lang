from enum import Enum, auto as _auto
import abc
import typing as t
from dataclasses import dataclass


from sijuiacion_lang.support import *


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


@adt_recog
@dataclass(frozen=True, order=True)
class Load(Instr):
    name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Store(Instr):
    name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Deref(Instr):
    name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class RefSet(Instr):
    name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Glob(Instr):
    name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Const(Instr):
    val:object
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Extern(Instr):
    code:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Pop(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class ROT(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class DUP(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Goto(Instr):
    label_name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class GotoEq(Instr):
    label_name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class GotoNEq(Instr):
    label_name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Label(Instr):
    label_name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class BlockAddr(Instr):
    label_name:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Indir(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Switch(Instr):
    table:t.Dict[int,
    str]
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Bin(Instr):
    op:BinOp
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class IBin(Instr):
    op:BinOp
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Un(Instr):
    op:UOp
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Cmp(Instr):
    op:Compare
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Attr(Instr):
    attr:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class AttrSet(Instr):
    attr:str
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Item(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class ItemSet(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Call(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Print(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class BuildList(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class BuildTuple(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class ListAppend(Instr):
    n:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Return(Instr):
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Line(Instr):
    no:int
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Defun(Instr):
    doc:str
    filename:str
    free:t.List[str]
    name:str
    args:t.List[str]
    suite:t.List[t.Union[Line,Instr]]
    pass


@adt_recog
@dataclass(frozen=True, order=True)
class Mod:
    filename:str
    tops:t.List[Instr]
    pass
