from bytecode import Instr, Bytecode, Label
from dataclasses import dataclass
import bytecode


@dataclass(order=True, frozen=True)
class NamedLabel(Label):
    name: str


WHY_CONTINUE = 0x0020

b = Bytecode()

b.extend([
    Instr("SETUP_LOOP", NamedLabel("l3")),
    Instr("LOAD_CONST", 0),
    Instr("DUP_TOP_TWO"),
    Instr("DUP_TOP_TWO"),
    Instr("DUP_TOP"),
    Instr("LOAD_FAST", "a"),
    Instr("LOAD_CONST", WHY_CONTINUE),
    Instr("END_FINALLY"),
    NamedLabel('l1'),
    Instr("LOAD_CONST", 10),
    Instr("PRINT_EXPR"),
    Instr("JUMP_ABSOLUTE", NamedLabel("l3")),
    NamedLabel('l2'),
    Instr("LOAD_CONST", 20),
    Instr("PRINT_EXPR"),
    Instr("JUMP_ABSOLUTE", NamedLabel("l3")),
    NamedLabel("l3"),
    Instr("LOAD_CONST", None),
    Instr("RETURN_VALUE")
])

b.argcount = 1
b.argnames.append('a')


def f(a):
    pass

b.to_concrete_bytecode
f.__code__ = b.to_code()
f(22)



converter = bytecode._ConvertBytecodeToConcrete(b)
concrete_codes = converter.to_concrete_bytecode(compute_jumps_passes=None)

for each in concrete_codes:
    print(each.name, each.arg)

print(converter.labels)
