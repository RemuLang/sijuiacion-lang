import typing as t
import bytecode
from bytecode import Instr, Bytecode, Label, ConcreteBytecode, ConcreteInstr
from dataclasses import dataclass
WHY_CONTINUE = 0x0020


@dataclass(order=True, frozen=True)
class NamedLabel(Label):
    name: str

@dataclass(order=True, frozen=True)
class LabelValue:
    name: str

@dataclass(order=True, frozen=True)
class LabelValueMap:
    map: t.Dict[int, str]

class BlockNotFoundError(Exception):
    pass


def label_to_offset(labels, label_name):
    label_offset = labels.get(label_name, None)
    if label_offset is None:
        raise BlockNotFoundError(label_name)
    return label_offset * 2

def resolve_blockaddr(bc: Bytecode):
    converter = bytecode._ConvertBytecodeToConcrete(bc)
    concrete_codes = converter.to_concrete_bytecode(compute_jumps_passes=None)
    labels = {k.name: v for k, v in converter.labels.items()}
    for each in concrete_codes:
        if isinstance(each, ConcreteInstr):
            if each.name != "LOAD_CONST":
                continue
            const_idx = each.arg
            const = concrete_codes.consts[const_idx]
            if not isinstance(const, (LabelValue, LabelValueMap)):
                continue
            if isinstance(const, LabelValue):
                concrete_codes.consts[const_idx] = label_to_offset(labels, const.name)
            else:
                # the branch indexed table
                switch_table = {k: label_to_offset(labels, v) for k, v in const.map.items()}
                concrete_codes.consts[const_idx] = switch_table

    return concrete_codes
