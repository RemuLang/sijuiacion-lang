# moshmosh?
# +quick-lambda
# +pipeline
# +pattern-matching

from sijuiacion_lang.blockaddr import resolve_blockaddr, NamedLabel, LabelValue, LabelValueMap, WHY_CONTINUE
from sijuiacion_lang import bytecode_instrs as I
from sijuiacion_lang import preserved_registers as PR
from sijuiacion_lang import sijuiacion as sij
from marshal import dumps as m_dumps
from types import ModuleType
import bytecode as bytec
import typing as t
import sys

PY38 = sys.version_info >= (3, 8)


def find_indir_targets(instrs):
    ret = set()
    for instr in instrs:
        if isinstance(instr, sij.BlockAddr):
            ret.add(instr.label_name)
        elif isinstance(instr, sij.Switch):
            ret.update(instr.table.values())
    return ret


class UnmarshalObject:
    __slots__ = []
    pass


class Lower:
    def __init__(self, env=None):
        self.env = env or ModuleType("<faker>")


    def lower(self, name, filename, lineno, doc, args, frees: t.List[str], instrs: t.List[sij.Instr]):
        """
        Before Python 3.8, indirect jumps via END_FINALLY
        should be wrapped in a SETUP_LOOP block
        """
        indir_targets = find_indir_targets(instrs)
        _line = lineno
        BytecodeInstrType = bytec.Instr
        const_pool = {}
        loc_maps = []
        inner_frees = set()

        def set_lineno(instr):
            if isinstance(instr, BytecodeInstrType):
                instr.lineno = _line
            return instr

        def gen_instrs():
            nonlocal _line
            if indir_targets and not PY38:
                yield I.LOAD_CONST(False)
                yield I.STORE_FAST(PR.REG_TEST_INDIR_JUMPED)
            for i, instr in enumerate(instrs):
                i = i + 1
                with match(instr):
                    if sij.Line(no):
                        _line = no
                    if sij.Load(name):
                        yield I.LOAD_FAST(name)
                    if sij.Store(name):
                        yield I.STORE_FAST(name)
                    if sij.Deref(name):
                        yield I.LOAD_DEREF(name)
                    if sij.RefSet(name):
                        yield I.STORE_DEREF(name)
                    if sij.Const(val):
                        contained = const_pool.get(val)
                        if not contained:
                            val_o = eval(val, self.env.__dict__)
                            try:
                                m_dumps(val_o)
                                contained = const_pool[val] = False, val_o
                            except ValueError:
                                val_o = [UnmarshalObject()]
                                contained = const_pool[val] = True, val_o
                        is_unmarshal_obj, val_o = contained
                        yield I.LOAD_CONST(val_o)
                        if is_unmarshal_obj:
                            yield I.LOAD_CONST(0)
                            yield I.BINARY(sij.BinOp.SUBSCR)

                    if sij.Pop():
                        yield I.POP_TOP()

                    if sij.ROT(n):
                        assert n in (2, 3), NotImplementedError
                        if n is 2:
                            yield I.ROT2()
                        else:
                            yield I.ROT3(3)
                    if sij.DUP(n):
                        # TODO
                        for each in range(n):
                            yield I.DUP()
                    if sij.Goto(name):
                        yield I.JUMP_ABSOLUTE(NamedLabel(name))
                    if sij.GotoEq(name):
                        yield I.POP_JUMP_IF_TRUE(NamedLabel(name))
                    if sij.GotoNEq(name):
                        yield I.POP_JUMP_IF_FALSE(NamedLabel(name))
                    if sij.Label(name):
                        yield NamedLabel(name)
                        if name in indir_targets and not PY38:
                            yield I.LOAD_FAST(PR.REG_TEST_INDIR_JUMPED)
                            yield I.POP_JUMP_IF_FALSE(NamedLabel(i))
                            yield I.POP_BLOCK()
                            yield I.LOAD_CONST(False)
                            yield I.STORE_FAST(PR.REG_TEST_INDIR_JUMPED)
                            yield NamedLabel(i)

                    if sij.BlockAddr(name):
                        label_as_value = LabelValue(name)
                        yield I.LOAD_CONST(label_as_value)
                    if sij.Indir():
                        if not PY38:
                            yield I.PUSH_BLOCK(i)
                            yield NamedLabel(i)
                            yield I.LOAD_CONST(True)
                            yield I.STORE_FAST(PR.REG_TEST_INDIR_JUMPED)
                        yield I.LOAD_CONST(WHY_CONTINUE)
                        yield I.INDIR()
                    if sij.Switch(table):
                        if None not in table:
                            yield I.LOAD_CONST(LabelValueMap(table))
                            yield I.ROT2()
                            yield I.BINARY(sij.BinOp.SUBSCR)
                        else:
                            # has default branch
                            val_o = [UnmarshalObject()]
                            const_pool['dict.get'] = True, val_o
                            yield I.LOAD_CONST(val_o)
                            yield I.LOAD_CONST(0)
                            yield I.BINARY(sij.BinOp.SUBSCR)
                            yield I.ROT2()
                            yield I.LOAD_CONST(LabelValueMap(table))
                            yield I.ROT2()
                            yield I.LOAD_CONST(LabelValue(table[None]))
                            yield I.CALL_FUNCTION(3)
                        if not PY38:
                            yield I.PUSH_BLOCK(i)
                            yield NamedLabel(i)
                            yield I.LOAD_CONST(True)
                            yield I.STORE_FAST(PR.REG_TEST_INDIR_JUMPED)
                        yield I.LOAD_CONST(WHY_CONTINUE)
                        yield I.INDIR()
                    if sij.Bin(bin_op):
                        yield I.BINARY(bin_op)
                    if sij.IBin(bin_op):
                        yield I.INPLACE_BINARY(bin_op)
                    if sij.Un(uop):
                        yield I.UNARY(uop)
                    if isinstance(sij.Compare):
                        yield instr.op
                    if sij.Attr(attr):
                        yield I.LOAD_ATTR(attr)
                    if sij.AttrSet(attr):
                        yield I.STORE_ATTR(attr)
                    if sij.Item():
                        yield I.BINARY(sij.BinOp.SUBSCR)
                    if sij.ItemSet():
                        yield I.STORE_SUBSCR()
                    if sij.Call(n):
                        yield I.CALL_FUNCTION(n)
                    if sij.Print():
                        yield I.PRINT_EXPR()
                    if sij.BuildList(n):
                        yield I.BUILD_LIST(n)
                    if sij.BuildTuple(n):
                        yield I.BUILD_TUPLE(n)
                    if sij.ListAppend(n):
                        yield I.LIST_APPEND(n)
                    if sij.Return():
                        yield I.RETURN_VALUE()
                    if sij.Defun(doc, filename_, frees, name, args, suite):
                        co_filename = filename_ or filename
                        has_free = bool(frees)
                        if has_free:
                            for freevar in frees:
                                yield I.LOAD_CLOSURE(freevar)
                            yield I.BUILD_TUPLE(len(frees))
                        code, loc_map = self.lower(name, co_filename, _line, doc, args, frees, suite)
                        inner_frees.update(code.co_freevars)
                        loc_maps.append((code, loc_map))
                        yield I.LOAD_CONST(code)
                        yield I.LOAD_CONST(name)
                        yield I.MAKE_FUNCTION(has_free)

        code = bytec.Bytecode([set_lineno(instr) for instr in gen_instrs()])
        code.argnames.extend(args)
        code.filename = filename
        code.first_lineno = lineno
        code.docstring = doc
        code.name = name
        code.argcount = len(args)
        cellvars = set()

        for each in code:
            if not isinstance(each, bytec.Instr):
                continue

            if not isinstance(each.arg, bytec.FreeVar):
                continue

            varname = each.arg.name

            if varname not in frees:
                each.arg = bytec.CellVar(varname)
                cellvars.add(varname)

        for varname in code.argnames:
            if varname in frees:
                cellvars.add(varname)

        code.freevars = frees
        code.cellvars = list(cellvars)
        stacksize = code.compute_stacksize()
        ccode = resolve_blockaddr(code)

        ccode.flags = bytec.flags.infer_flags(ccode)
        pycode = ccode.to_code(stacksize)
        unmarshall_objs = {}
        consts = pycode.co_consts
        for val_str, (is_unmarshal_obj, val_o) in const_pool.items():
            if is_unmarshal_obj:
                unmarshall_objs[val_str] = consts.index(val_o)
                val_o.pop()

        nested_unmarshal_info = []
        for code, loc_map in loc_maps:
            nested_unmarshal_info.append((consts.index(code), loc_map))

        return pycode, (unmarshall_objs, nested_unmarshal_info)
