from bytecode import Instr, Bytecode, Label, ConcreteInstr
from sijuiacion_lang.blockaddr import resolve_blockaddr, NamedLabel, LabelValue
from dataclasses import dataclass
import bytecode

WHY_CONTINUE = 0x0020

b = Bytecode()

class Indir(Instr):
    name = "END_FINALLY"

    def stack_effect(self, jump=None):
        return -2

    def __repr__(self):
        return "Indirect"
    
b.extend([

#    Instr("LOAD_CONST", 0),
#    Instr("DUP_TOP_TWO"),
#    Instr("DUP_TOP"),
    Instr("LOAD_CONST", LabelValue("l2")),
    Instr("LOAD_CONST", WHY_CONTINUE),
    Instr("SETUP_LOOP", NamedLabel("l1")),
    Instr("END_FINALLY"),
    NamedLabel('l1'),
    Instr("LOAD_CONST", 10),
    Instr("PRINT_EXPR"),
    # Instr("JUMP_ABSOLUTE", NamedLabel("l3")),
    NamedLabel('l2'),
    Instr("LOAD_CONST", 20),
    Instr("PRINT_EXPR"),
    # Instr("JUMP_ABSOLUTE", NamedLabel("l3")),
    NamedLabel("l3"),
    Instr("LOAD_CONST", None),
    Instr("RETURN_VALUE")
])

def f():
    pas

b.argcount = 1
b.argnames.append("a")

for i, each in enumerate(b):
    if each.name == Indir.name:
        break

b[i] = Indir(each.name, lineno=each.lineno)
size = b.compute_stacksize()
code = resolve_blockaddr(b)

f.__code__ = code.to_code(stacksize=size)
import dis
dis.dis(f.__code__)
f(1)



# converter = bytecode._ConvertBytecodeToConcrete(b)
# concrete_codes = converter.to_concrete_bytecode(compute_jumps_passes=None)

# for each in concrete_codes:
#     print(each.name, each.arg)

# print(converter.labels)
