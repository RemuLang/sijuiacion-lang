from bytecode import Instr, Bytecode, Label, ConcreteBytecode, ConcreteInstr
import bytecode
from dataclasses import dataclass
WHY_CONTINUE = 0x0020


@dataclass(order=True, frozen=True)
class NamedLabel(Label):
    name: str


class BlockNotFoundError(Exception):
    pass


def resolve_blockaddr(concreate_bytecode: ConcreteBytecode):
    converter = bytecode._ConvertBytecodeToConcrete(concreate_bytecode)
    labels = converter.labels
    concrete_codes = converter.to_concrete_bytecode(compute_jumps_passes=None)
    for each in concreate_bytecode:
        if isinstance(each, ConcreteInstr):
            if each.name != "LOAD_CONST":
                continue
            const_idx = each.arg
            if not isinstance(concreate_bytecode.consts[const_idx], NamedLabel):
                continue

            label = concreate_bytecode.consts[const_idx]
            label_offset = labels.get(label, None)
            if label_offset is None:
                raise BlockNotFoundError(label)
            concreate_bytecode.consts[const_idx] = label_offset
