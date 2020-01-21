from sijuiacion_lang import instr_names
from sijuiacion_lang.bytecode_patch import IndirectJump
from sijuiacion_lang.blockaddr import NamedLabel
from bytecode import Instr, FreeVar


def LOAD_CONST(val):
    return Instr(instr_names.LOAD_CONST, val)


def LOAD_FAST(n):
    return Instr(instr_names.LOAD_FAST, n)


def LOAD_GLOBAL(n):
    return Instr(instr_names.LOAD_GLOBAL, n)


def STORE_GLOBAL(n):
    return Instr(instr_names.STORE_GLOBAL, n)


def COMPARE_OP(n):
    return Instr(instr_names.COMPARE_OP, n)


def RAISE_VARARGS(i):
    return Instr(instr_names.RAISE_VARARGS, i)


def LOAD_DEREF(n):
    # will resolve free/cell var later
    return Instr(instr_names.LOAD_DEREF, FreeVar(n))


def STORE_FAST(n):
    return Instr(instr_names.STORE_FAST, n)


def STORE_DEREF(n):
    # will resolve free/cell var later
    return Instr(instr_names.STORE_DEREF, FreeVar(n))


def LOAD_CLOSURE(n):
    # will resolve free/cell var later
    return Instr(instr_names.LOAD_CLOSURE, FreeVar(n))


def POP_TOP():
    return Instr(instr_names.POP_TOP)


def ROT3():
    return Instr(instr_names.ROT_THREE)


def ROT2():
    return Instr(instr_names.ROT_TWO)


def DUP():
    return Instr(instr_names.DUP_TOP)


def DUP2():
    return Instr(instr_names.DUP_TOP_TWO)


def POP_JUMP_IF_TRUE(i):
    return Instr(instr_names.POP_JUMP_IF_TRUE, i)


def POP_JUMP_IF_FALSE(i):
    return Instr(instr_names.POP_JUMP_IF_FALSE, i)


def JUMP_ABSOLUTE(i):
    return Instr(instr_names.JUMP_ABSOLUTE, i)


def INDIR():
    return IndirectJump("END_FINALLY")


def BINARY(bin_op):
    return Instr('BINARY_' + bin_op.name)


def INPLACE_BINARY(bin_op):
    return Instr('INPLACE_' + bin_op.name)


def UNARY(u_op):
    return Instr('UNARY_' + u_op.name)


def UNPACK_SEQUENCE(n: int):
    return Instr(instr_names.UNPACK_SEQUENCE, n)


def LOAD_ATTR(n):
    return Instr(instr_names.LOAD_ATTR, n)


def STORE_ATTR(n):
    return Instr(instr_names.STORE_ATTR, n)


def STORE_SUBSCR():
    return Instr(instr_names.STORE_SUBSCR)


def CALL_FUNCTION(n):
    return Instr(instr_names.CALL_FUNCTION, n)


def BUILD_LIST(n):
    return Instr(instr_names.BUILD_LIST, n)


def BUILD_TUPLE(n):
    return Instr(instr_names.BUILD_TUPLE, n)


def LIST_APPEND(i):
    return Instr(instr_names.LIST_APPEND, i)


def RETURN_VALUE():
    return Instr(instr_names.RETURN_VALUE)


def MAKE_FUNCTION(has_free):
    assert isinstance(has_free, bool)
    if has_free:
        return Instr(instr_names.MAKE_FUNCTION, 0x08)
    return Instr(instr_names.MAKE_FUNCTION, 0)


def PRINT_EXPR():
    return Instr(instr_names.PRINT_EXPR)


# for Python 3.8-
def PUSH_BLOCK(i):
    return Instr(instr_names.SETUP_LOOP, NamedLabel(i))


def POP_BLOCK():
    return Instr(instr_names.POP_BLOCK)
