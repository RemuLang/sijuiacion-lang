from sijuiacion_lang.blockaddr import resolve_blockaddr, NamedLabel, LabelValue, LabelValueMap, WHY_CONTINUE
from sijuiacion_lang import bytecode_instrs as I
from sijuiacion_lang import preserved_registers as PR
from sijuiacion_lang import sijuiacion as sij
from sijuiacion_lang.moshmosh_rts import NotExhaustive
from marshal import dumps as m_dumps
from types import ModuleType
import bytecode as bytec
import typing as t
import sys
PY38 = (sys.version_info >= (3, 8))


def find_indir_targets(instrs):
    ret = set()
    for instr in instrs:
        if isinstance(instr, sij.BlockAddr):
            ret.add(instr.label_name)
        elif isinstance(instr, sij.Switch):
            ret.update(instr.table.values())
    return ret


class UnmarshalObject():
    __slots__ = []
    pass


class Lower():
    def __init__(self, env=None):
        self.env = (env or ModuleType('<faker>'))

    def lower(self, name, filename, lineno, doc, args, frees: t.List[str],
              instrs: t.List[sij.Instr]):
        '\n        Before Python 3.8, indirect jumps via END_FINALLY\n        should be wrapped in a SETUP_LOOP block\n        '
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
            if (indir_targets and (not PY38)):
                (yield I.LOAD_CONST(False))
                (yield I.STORE_FAST(PR.REG_TEST_INDIR_JUMPED))
            for (i, instr) in enumerate(instrs):
                i = (i + 1)
                if isinstance(instr, sij.Line):
                    _line = instr.no
                    continue
                if isinstance(instr, sij.Pop):
                    (yield I.POP_TOP())
                    continue
                _gensym_0 = instr
                _gensym_1 = sij.Cmp.__match__(1, _gensym_0)
                if (_gensym_1 is None):
                    _gensym_2 = None
                elif isinstance(_gensym_1, tuple):
                    if (len(_gensym_1) is 1):
                        _gensym_3 = _gensym_1[0]
                        op = _gensym_3
                        _gensym_2 = ()
                        (yield I.COMPARE_OP(op))
                    else:
                        _gensym_2 = None
                else:
                    _gensym_2 = None
                if (_gensym_2 is None):
                    _gensym_4 = sij.Glob.__match__(1, _gensym_0)
                    if (_gensym_4 is None):
                        _gensym_2 = None
                    elif isinstance(_gensym_4, tuple):
                        if (len(_gensym_4) is 1):
                            _gensym_5 = _gensym_4[0]
                            name = _gensym_5
                            _gensym_2 = ()
                            (yield I.LOAD_GLOBAL(name))
                        else:
                            _gensym_2 = None
                    else:
                        _gensym_2 = None
                    if (_gensym_2 is None):
                        _gensym_6 = sij.GlobSet.__match__(1, _gensym_0)
                        if (_gensym_6 is None):
                            _gensym_2 = None
                        elif isinstance(_gensym_6, tuple):
                            if (len(_gensym_6) is 1):
                                _gensym_7 = _gensym_6[0]
                                name = _gensym_7
                                _gensym_2 = ()
                                (yield I.STORE_GLOBAL(name))
                            else:
                                _gensym_2 = None
                        else:
                            _gensym_2 = None
                        if (_gensym_2 is None):
                            _gensym_8 = sij.Load.__match__(1, _gensym_0)
                            if (_gensym_8 is None):
                                _gensym_2 = None
                            elif isinstance(_gensym_8, tuple):
                                if (len(_gensym_8) is 1):
                                    _gensym_9 = _gensym_8[0]
                                    name = _gensym_9
                                    _gensym_2 = ()
                                    (yield I.LOAD_FAST(name))
                                else:
                                    _gensym_2 = None
                            else:
                                _gensym_2 = None
                            if (_gensym_2 is None):
                                _gensym_10 = sij.Store.__match__(1, _gensym_0)
                                if (_gensym_10 is None):
                                    _gensym_2 = None
                                elif isinstance(_gensym_10, tuple):
                                    if (len(_gensym_10) is 1):
                                        _gensym_11 = _gensym_10[0]
                                        name = _gensym_11
                                        _gensym_2 = ()
                                        (yield I.STORE_FAST(name))
                                    else:
                                        _gensym_2 = None
                                else:
                                    _gensym_2 = None
                                if (_gensym_2 is None):
                                    _gensym_12 = sij.Deref.__match__(
                                        1, _gensym_0)
                                    if (_gensym_12 is None):
                                        _gensym_2 = None
                                    elif isinstance(_gensym_12, tuple):
                                        if (len(_gensym_12) is 1):
                                            _gensym_13 = _gensym_12[0]
                                            name = _gensym_13
                                            _gensym_2 = ()
                                            (yield I.LOAD_DEREF(name))
                                        else:
                                            _gensym_2 = None
                                    else:
                                        _gensym_2 = None
                                    if (_gensym_2 is None):
                                        _gensym_14 = sij.RefSet.__match__(
                                            1, _gensym_0)
                                        if (_gensym_14 is None):
                                            _gensym_2 = None
                                        elif isinstance(_gensym_14, tuple):
                                            if (len(_gensym_14) is 1):
                                                _gensym_15 = _gensym_14[0]
                                                name = _gensym_15
                                                _gensym_2 = ()
                                                (yield I.STORE_DEREF(name))
                                            else:
                                                _gensym_2 = None
                                        else:
                                            _gensym_2 = None
                                        if (_gensym_2 is None):
                                            _gensym_16 = sij.SimpleRaise.__match__(
                                                0, _gensym_0)
                                            if (_gensym_16 is None):
                                                _gensym_2 = None
                                            elif isinstance(_gensym_16, tuple):
                                                if (len(_gensym_16) is 0):
                                                    _gensym_2 = ()
                                                    (yield I.RAISE_VARARGS(1))
                                                else:
                                                    _gensym_2 = None
                                            else:
                                                _gensym_2 = None
                                            if (_gensym_2 is None):
                                                _gensym_17 = sij.Unpack.__match__(
                                                    1, _gensym_0)
                                                if (_gensym_17 is None):
                                                    _gensym_2 = None
                                                elif isinstance(
                                                        _gensym_17, tuple):
                                                    if (len(_gensym_17) is 1):
                                                        _gensym_18 = _gensym_17[
                                                            0]
                                                        n = _gensym_18
                                                        _gensym_2 = ()
                                                        (yield
                                                         I.UNPACK_SEQUENCE(n))
                                                    else:
                                                        _gensym_2 = None
                                                else:
                                                    _gensym_2 = None
                                                if (_gensym_2 is None):
                                                    _gensym_19 = sij.Const.__match__(
                                                        1, _gensym_0)
                                                    if (_gensym_19 is None):
                                                        _gensym_2 = None
                                                    elif isinstance(
                                                            _gensym_19, tuple):
                                                        if (len(_gensym_19) is
                                                                1):
                                                            _gensym_20 = _gensym_19[
                                                                0]
                                                            val = _gensym_20
                                                            _gensym_2 = ()
                                                            (yield
                                                             I.LOAD_CONST(val))
                                                        else:
                                                            _gensym_2 = None
                                                    else:
                                                        _gensym_2 = None
                                                    if (_gensym_2 is None):
                                                        _gensym_21 = sij.Extern.__match__(
                                                            1, _gensym_0)
                                                        if (_gensym_21 is
                                                                None):
                                                            _gensym_2 = None
                                                        elif isinstance(
                                                                _gensym_21,
                                                                tuple):
                                                            if (len(_gensym_21)
                                                                    is 1):
                                                                _gensym_22 = _gensym_21[
                                                                    0]
                                                                val = _gensym_22
                                                                _gensym_2 = ()
                                                                contained = const_pool.get(
                                                                    val)
                                                                if (not contained
                                                                    ):
                                                                    val_o = eval(
                                                                        val,
                                                                        self.
                                                                        env.
                                                                        __dict__
                                                                    )
                                                                    try:
                                                                        m_dumps(
                                                                            val_o
                                                                        )
                                                                        contained = const_pool[
                                                                            val] = (
                                                                                False,
                                                                                val_o
                                                                            )
                                                                    except ValueError:
                                                                        val_o = [
                                                                            UnmarshalObject(
                                                                            )
                                                                        ]
                                                                        contained = const_pool[
                                                                            val] = (
                                                                                True,
                                                                                val_o
                                                                            )
                                                                (is_unmarshal_obj,
                                                                 val_o
                                                                 ) = contained
                                                                (yield
                                                                 I.LOAD_CONST(
                                                                     val_o))
                                                                if is_unmarshal_obj:
                                                                    (yield I.
                                                                     LOAD_CONST(
                                                                         0))
                                                                    (yield
                                                                     I.BINARY(
                                                                         sij.
                                                                         BinOp.
                                                                         SUBSCR
                                                                     ))
                                                            else:
                                                                _gensym_2 = None
                                                        else:
                                                            _gensym_2 = None
                                                        if (_gensym_2 is None):
                                                            _gensym_23 = sij.ROT.__match__(
                                                                1, _gensym_0)
                                                            if (_gensym_23 is
                                                                    None):
                                                                _gensym_2 = None
                                                            elif isinstance(
                                                                    _gensym_23,
                                                                    tuple):
                                                                if (len(_gensym_23
                                                                        ) is
                                                                        1):
                                                                    _gensym_24 = _gensym_23[
                                                                        0]
                                                                    n = _gensym_24
                                                                    _gensym_2 = (
                                                                    )
                                                                    assert (
                                                                        n in (
                                                                            2,
                                                                            3)
                                                                    ), NotImplementedError
                                                                    if (n is
                                                                            2):
                                                                        (yield
                                                                         I.
                                                                         ROT2(
                                                                         ))
                                                                    else:
                                                                        (yield
                                                                         I.
                                                                         ROT3(
                                                                         ))
                                                                else:
                                                                    _gensym_2 = None
                                                            else:
                                                                _gensym_2 = None
                                                            if (_gensym_2 is
                                                                    None):
                                                                _gensym_25 = sij.DUP.__match__(
                                                                    1,
                                                                    _gensym_0)
                                                                if (_gensym_25
                                                                        is
                                                                        None):
                                                                    _gensym_2 = None
                                                                elif isinstance(
                                                                        _gensym_25,
                                                                        tuple):
                                                                    if (len(_gensym_25
                                                                            )
                                                                            is
                                                                            1):
                                                                        _gensym_26 = _gensym_25[
                                                                            0]
                                                                        n = _gensym_26
                                                                        _gensym_2 = (
                                                                        )
                                                                        for each in range(
                                                                                n
                                                                        ):
                                                                            (yield
                                                                             I.
                                                                             DUP(
                                                                             ))
                                                                    else:
                                                                        _gensym_2 = None
                                                                else:
                                                                    _gensym_2 = None
                                                                if (_gensym_2
                                                                        is
                                                                        None):
                                                                    _gensym_27 = sij.Goto.__match__(
                                                                        1,
                                                                        _gensym_0
                                                                    )
                                                                    if (_gensym_27
                                                                            is
                                                                            None
                                                                        ):
                                                                        _gensym_2 = None
                                                                    elif isinstance(
                                                                            _gensym_27,
                                                                            tuple
                                                                    ):
                                                                        if (len(
                                                                                _gensym_27
                                                                        ) is 1
                                                                            ):
                                                                            _gensym_28 = _gensym_27[
                                                                                0]
                                                                            name = _gensym_28
                                                                            _gensym_2 = (
                                                                            )
                                                                            (yield
                                                                             I.
                                                                             JUMP_ABSOLUTE(
                                                                                 NamedLabel(
                                                                                     name
                                                                                 )
                                                                             ))
                                                                        else:
                                                                            _gensym_2 = None
                                                                    else:
                                                                        _gensym_2 = None
                                                                    if (_gensym_2
                                                                            is
                                                                            None
                                                                        ):
                                                                        _gensym_29 = sij.GotoEq.__match__(
                                                                            1,
                                                                            _gensym_0
                                                                        )
                                                                        if (_gensym_29
                                                                                is
                                                                                None
                                                                            ):
                                                                            _gensym_2 = None
                                                                        elif isinstance(
                                                                                _gensym_29,
                                                                                tuple
                                                                        ):
                                                                            if (len(
                                                                                    _gensym_29
                                                                            ) is 1
                                                                                ):
                                                                                _gensym_30 = _gensym_29[
                                                                                    0]
                                                                                name = _gensym_30
                                                                                _gensym_2 = (
                                                                                )
                                                                                (yield
                                                                                 I
                                                                                 .
                                                                                 POP_JUMP_IF_TRUE(
                                                                                     NamedLabel(
                                                                                         name
                                                                                     )
                                                                                 )
                                                                                 )
                                                                            else:
                                                                                _gensym_2 = None
                                                                        else:
                                                                            _gensym_2 = None
                                                                        if (_gensym_2
                                                                                is
                                                                                None
                                                                            ):
                                                                            _gensym_31 = sij.GotoNEq.__match__(
                                                                                1,
                                                                                _gensym_0
                                                                            )
                                                                            if (
                                                                                    _gensym_31
                                                                                    is
                                                                                    None
                                                                            ):
                                                                                _gensym_2 = None
                                                                            elif isinstance(
                                                                                    _gensym_31,
                                                                                    tuple
                                                                            ):
                                                                                if (len(
                                                                                        _gensym_31
                                                                                ) is 1
                                                                                    ):
                                                                                    _gensym_32 = _gensym_31[
                                                                                        0]
                                                                                    name = _gensym_32
                                                                                    _gensym_2 = (
                                                                                    )
                                                                                    (yield
                                                                                     I
                                                                                     .
                                                                                     POP_JUMP_IF_FALSE(
                                                                                         NamedLabel(
                                                                                             name
                                                                                         )
                                                                                     )
                                                                                     )
                                                                                else:
                                                                                    _gensym_2 = None
                                                                            else:
                                                                                _gensym_2 = None
                                                                            if (
                                                                                    _gensym_2
                                                                                    is
                                                                                    None
                                                                            ):
                                                                                _gensym_33 = sij.Label.__match__(
                                                                                    1,
                                                                                    _gensym_0
                                                                                )
                                                                                if (
                                                                                        _gensym_33
                                                                                        is
                                                                                        None
                                                                                ):
                                                                                    _gensym_2 = None
                                                                                elif isinstance(
                                                                                        _gensym_33,
                                                                                        tuple
                                                                                ):
                                                                                    if (len(
                                                                                            _gensym_33
                                                                                    ) is 1
                                                                                        ):
                                                                                        _gensym_34 = _gensym_33[
                                                                                            0]
                                                                                        name = _gensym_34
                                                                                        _gensym_2 = (
                                                                                        )
                                                                                        (yield
                                                                                         NamedLabel(
                                                                                             name
                                                                                         )
                                                                                         )
                                                                                        if (
                                                                                            (name
                                                                                             in
                                                                                             indir_targets
                                                                                             ) and
                                                                                            (not PY38
                                                                                             )
                                                                                        ):
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             LOAD_FAST(
                                                                                                 PR
                                                                                                 .
                                                                                                 REG_TEST_INDIR_JUMPED
                                                                                             )
                                                                                             )
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             POP_JUMP_IF_FALSE(
                                                                                                 NamedLabel(
                                                                                                     i
                                                                                                 )
                                                                                             )
                                                                                             )
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             POP_BLOCK(
                                                                                             )
                                                                                             )
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             LOAD_CONST(
                                                                                                 False
                                                                                             )
                                                                                             )
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             STORE_FAST(
                                                                                                 PR
                                                                                                 .
                                                                                                 REG_TEST_INDIR_JUMPED
                                                                                             )
                                                                                             )
                                                                                            (yield
                                                                                             NamedLabel(
                                                                                                 i
                                                                                             )
                                                                                             )
                                                                                    else:
                                                                                        _gensym_2 = None
                                                                                else:
                                                                                    _gensym_2 = None
                                                                                if (
                                                                                        _gensym_2
                                                                                        is
                                                                                        None
                                                                                ):
                                                                                    _gensym_35 = sij.BlockAddr.__match__(
                                                                                        1,
                                                                                        _gensym_0
                                                                                    )
                                                                                    if (
                                                                                            _gensym_35
                                                                                            is
                                                                                            None
                                                                                    ):
                                                                                        _gensym_2 = None
                                                                                    elif isinstance(
                                                                                            _gensym_35,
                                                                                            tuple
                                                                                    ):
                                                                                        if (len(
                                                                                                _gensym_35
                                                                                        ) is 1
                                                                                            ):
                                                                                            _gensym_36 = _gensym_35[
                                                                                                0]
                                                                                            name = _gensym_36
                                                                                            _gensym_2 = (
                                                                                            )
                                                                                            label_as_value = LabelValue(
                                                                                                name
                                                                                            )
                                                                                            (yield
                                                                                             I
                                                                                             .
                                                                                             LOAD_CONST(
                                                                                                 label_as_value
                                                                                             )
                                                                                             )
                                                                                        else:
                                                                                            _gensym_2 = None
                                                                                    else:
                                                                                        _gensym_2 = None
                                                                                    if (
                                                                                            _gensym_2
                                                                                            is
                                                                                            None
                                                                                    ):
                                                                                        _gensym_37 = sij.Indir.__match__(
                                                                                            0,
                                                                                            _gensym_0
                                                                                        )
                                                                                        if (
                                                                                                _gensym_37
                                                                                                is
                                                                                                None
                                                                                        ):
                                                                                            _gensym_2 = None
                                                                                        elif isinstance(
                                                                                                _gensym_37,
                                                                                                tuple
                                                                                        ):
                                                                                            if (len(
                                                                                                    _gensym_37
                                                                                            ) is 0
                                                                                                ):
                                                                                                _gensym_2 = (
                                                                                                )
                                                                                                if (not PY38
                                                                                                    ):
                                                                                                    (yield
                                                                                                     I
                                                                                                     .
                                                                                                     PUSH_BLOCK(
                                                                                                         i
                                                                                                     )
                                                                                                     )
                                                                                                    (yield
                                                                                                     NamedLabel(
                                                                                                         i
                                                                                                     )
                                                                                                     )
                                                                                                    (yield
                                                                                                     I
                                                                                                     .
                                                                                                     LOAD_CONST(
                                                                                                         True
                                                                                                     )
                                                                                                     )
                                                                                                    (yield
                                                                                                     I
                                                                                                     .
                                                                                                     STORE_FAST(
                                                                                                         PR
                                                                                                         .
                                                                                                         REG_TEST_INDIR_JUMPED
                                                                                                     )
                                                                                                     )
                                                                                                (yield
                                                                                                 I
                                                                                                 .
                                                                                                 LOAD_CONST(
                                                                                                     WHY_CONTINUE
                                                                                                 )
                                                                                                 )
                                                                                                (yield
                                                                                                 I
                                                                                                 .
                                                                                                 INDIR(
                                                                                                 )
                                                                                                 )
                                                                                            else:
                                                                                                _gensym_2 = None
                                                                                        else:
                                                                                            _gensym_2 = None
                                                                                        if (
                                                                                                _gensym_2
                                                                                                is
                                                                                                None
                                                                                        ):
                                                                                            _gensym_38 = sij.Switch.__match__(
                                                                                                1,
                                                                                                _gensym_0
                                                                                            )
                                                                                            if (
                                                                                                    _gensym_38
                                                                                                    is
                                                                                                    None
                                                                                            ):
                                                                                                _gensym_2 = None
                                                                                            elif isinstance(
                                                                                                    _gensym_38,
                                                                                                    tuple
                                                                                            ):
                                                                                                if (len(
                                                                                                        _gensym_38
                                                                                                ) is 1
                                                                                                    ):
                                                                                                    _gensym_39 = _gensym_38[
                                                                                                        0]
                                                                                                    table = _gensym_39
                                                                                                    _gensym_2 = (
                                                                                                    )
                                                                                                    if (
                                                                                                            None
                                                                                                            not in
                                                                                                            table
                                                                                                    ):
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             LabelValueMap(
                                                                                                                 table
                                                                                                             )
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         ROT2(
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         BINARY(
                                                                                                             sij
                                                                                                             .
                                                                                                             BinOp
                                                                                                             .
                                                                                                             SUBSCR
                                                                                                         )
                                                                                                         )
                                                                                                    else:
                                                                                                        val_o = [
                                                                                                            UnmarshalObject(
                                                                                                            )
                                                                                                        ]
                                                                                                        const_pool[
                                                                                                            'dict.get'] = (
                                                                                                                True,
                                                                                                                val_o
                                                                                                            )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             val_o
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             0
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         BINARY(
                                                                                                             sij
                                                                                                             .
                                                                                                             BinOp
                                                                                                             .
                                                                                                             SUBSCR
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         ROT2(
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             LabelValueMap(
                                                                                                                 table
                                                                                                             )
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         ROT2(
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             LabelValue(
                                                                                                                 table[
                                                                                                                     None]
                                                                                                             )
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         CALL_FUNCTION(
                                                                                                             3
                                                                                                         )
                                                                                                         )
                                                                                                    if (not PY38
                                                                                                        ):
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         PUSH_BLOCK(
                                                                                                             i
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         NamedLabel(
                                                                                                             i
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         LOAD_CONST(
                                                                                                             True
                                                                                                         )
                                                                                                         )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         STORE_FAST(
                                                                                                             PR
                                                                                                             .
                                                                                                             REG_TEST_INDIR_JUMPED
                                                                                                         )
                                                                                                         )
                                                                                                    (yield
                                                                                                     I
                                                                                                     .
                                                                                                     LOAD_CONST(
                                                                                                         WHY_CONTINUE
                                                                                                     )
                                                                                                     )
                                                                                                    (yield
                                                                                                     I
                                                                                                     .
                                                                                                     INDIR(
                                                                                                     )
                                                                                                     )
                                                                                                else:
                                                                                                    _gensym_2 = None
                                                                                            else:
                                                                                                _gensym_2 = None
                                                                                            if (
                                                                                                    _gensym_2
                                                                                                    is
                                                                                                    None
                                                                                            ):
                                                                                                _gensym_40 = sij.Bin.__match__(
                                                                                                    1,
                                                                                                    _gensym_0
                                                                                                )
                                                                                                if (
                                                                                                        _gensym_40
                                                                                                        is
                                                                                                        None
                                                                                                ):
                                                                                                    _gensym_2 = None
                                                                                                elif isinstance(
                                                                                                        _gensym_40,
                                                                                                        tuple
                                                                                                ):
                                                                                                    if (len(
                                                                                                            _gensym_40
                                                                                                    ) is 1
                                                                                                        ):
                                                                                                        _gensym_41 = _gensym_40[
                                                                                                            0]
                                                                                                        bin_op = _gensym_41
                                                                                                        _gensym_2 = (
                                                                                                        )
                                                                                                        (yield
                                                                                                         I
                                                                                                         .
                                                                                                         BINARY(
                                                                                                             bin_op
                                                                                                         )
                                                                                                         )
                                                                                                    else:
                                                                                                        _gensym_2 = None
                                                                                                else:
                                                                                                    _gensym_2 = None
                                                                                                if (
                                                                                                        _gensym_2
                                                                                                        is
                                                                                                        None
                                                                                                ):
                                                                                                    _gensym_42 = sij.IBin.__match__(
                                                                                                        1,
                                                                                                        _gensym_0
                                                                                                    )
                                                                                                    if (
                                                                                                            _gensym_42
                                                                                                            is
                                                                                                            None
                                                                                                    ):
                                                                                                        _gensym_2 = None
                                                                                                    elif isinstance(
                                                                                                            _gensym_42,
                                                                                                            tuple
                                                                                                    ):
                                                                                                        if (len(
                                                                                                                _gensym_42
                                                                                                        ) is 1
                                                                                                            ):
                                                                                                            _gensym_43 = _gensym_42[
                                                                                                                0]
                                                                                                            bin_op = _gensym_43
                                                                                                            _gensym_2 = (
                                                                                                            )
                                                                                                            (yield
                                                                                                             I
                                                                                                             .
                                                                                                             INPLACE_BINARY(
                                                                                                                 bin_op
                                                                                                             )
                                                                                                             )
                                                                                                        else:
                                                                                                            _gensym_2 = None
                                                                                                    else:
                                                                                                        _gensym_2 = None
                                                                                                    if (
                                                                                                            _gensym_2
                                                                                                            is
                                                                                                            None
                                                                                                    ):
                                                                                                        _gensym_44 = sij.Un.__match__(
                                                                                                            1,
                                                                                                            _gensym_0
                                                                                                        )
                                                                                                        if (
                                                                                                                _gensym_44
                                                                                                                is
                                                                                                                None
                                                                                                        ):
                                                                                                            _gensym_2 = None
                                                                                                        elif isinstance(
                                                                                                                _gensym_44,
                                                                                                                tuple
                                                                                                        ):
                                                                                                            if (len(
                                                                                                                    _gensym_44
                                                                                                            ) is 1
                                                                                                                ):
                                                                                                                _gensym_45 = _gensym_44[
                                                                                                                    0]
                                                                                                                uop = _gensym_45
                                                                                                                _gensym_2 = (
                                                                                                                )
                                                                                                                (yield
                                                                                                                 I
                                                                                                                 .
                                                                                                                 UNARY(
                                                                                                                     uop
                                                                                                                 )
                                                                                                                 )
                                                                                                            else:
                                                                                                                _gensym_2 = None
                                                                                                        else:
                                                                                                            _gensym_2 = None
                                                                                                        if (
                                                                                                                _gensym_2
                                                                                                                is
                                                                                                                None
                                                                                                        ):
                                                                                                            _gensym_46 = sij.Attr.__match__(
                                                                                                                1,
                                                                                                                _gensym_0
                                                                                                            )
                                                                                                            if (
                                                                                                                    _gensym_46
                                                                                                                    is
                                                                                                                    None
                                                                                                            ):
                                                                                                                _gensym_2 = None
                                                                                                            elif isinstance(
                                                                                                                    _gensym_46,
                                                                                                                    tuple
                                                                                                            ):
                                                                                                                if (len(
                                                                                                                        _gensym_46
                                                                                                                ) is 1
                                                                                                                    ):
                                                                                                                    _gensym_47 = _gensym_46[
                                                                                                                        0]
                                                                                                                    attr = _gensym_47
                                                                                                                    _gensym_2 = (
                                                                                                                    )
                                                                                                                    (yield
                                                                                                                     I
                                                                                                                     .
                                                                                                                     LOAD_ATTR(
                                                                                                                         attr
                                                                                                                     )
                                                                                                                     )
                                                                                                                else:
                                                                                                                    _gensym_2 = None
                                                                                                            else:
                                                                                                                _gensym_2 = None
                                                                                                            if (
                                                                                                                    _gensym_2
                                                                                                                    is
                                                                                                                    None
                                                                                                            ):
                                                                                                                _gensym_48 = sij.AttrSet.__match__(
                                                                                                                    1,
                                                                                                                    _gensym_0
                                                                                                                )
                                                                                                                if (
                                                                                                                        _gensym_48
                                                                                                                        is
                                                                                                                        None
                                                                                                                ):
                                                                                                                    _gensym_2 = None
                                                                                                                elif isinstance(
                                                                                                                        _gensym_48,
                                                                                                                        tuple
                                                                                                                ):
                                                                                                                    if (len(
                                                                                                                            _gensym_48
                                                                                                                    ) is 1
                                                                                                                        ):
                                                                                                                        _gensym_49 = _gensym_48[
                                                                                                                            0]
                                                                                                                        attr = _gensym_49
                                                                                                                        _gensym_2 = (
                                                                                                                        )
                                                                                                                        (yield
                                                                                                                         I
                                                                                                                         .
                                                                                                                         STORE_ATTR(
                                                                                                                             attr
                                                                                                                         )
                                                                                                                         )
                                                                                                                    else:
                                                                                                                        _gensym_2 = None
                                                                                                                else:
                                                                                                                    _gensym_2 = None
                                                                                                                if (
                                                                                                                        _gensym_2
                                                                                                                        is
                                                                                                                        None
                                                                                                                ):
                                                                                                                    _gensym_50 = sij.Item.__match__(
                                                                                                                        0,
                                                                                                                        _gensym_0
                                                                                                                    )
                                                                                                                    if (
                                                                                                                            _gensym_50
                                                                                                                            is
                                                                                                                            None
                                                                                                                    ):
                                                                                                                        _gensym_2 = None
                                                                                                                    elif isinstance(
                                                                                                                            _gensym_50,
                                                                                                                            tuple
                                                                                                                    ):
                                                                                                                        if (len(
                                                                                                                                _gensym_50
                                                                                                                        ) is 0
                                                                                                                            ):
                                                                                                                            _gensym_2 = (
                                                                                                                            )
                                                                                                                            (yield
                                                                                                                             I
                                                                                                                             .
                                                                                                                             BINARY(
                                                                                                                                 sij
                                                                                                                                 .
                                                                                                                                 BinOp
                                                                                                                                 .
                                                                                                                                 SUBSCR
                                                                                                                             )
                                                                                                                             )
                                                                                                                        else:
                                                                                                                            _gensym_2 = None
                                                                                                                    else:
                                                                                                                        _gensym_2 = None
                                                                                                                    if (
                                                                                                                            _gensym_2
                                                                                                                            is
                                                                                                                            None
                                                                                                                    ):
                                                                                                                        _gensym_51 = sij.ItemSet.__match__(
                                                                                                                            0,
                                                                                                                            _gensym_0
                                                                                                                        )
                                                                                                                        if (
                                                                                                                                _gensym_51
                                                                                                                                is
                                                                                                                                None
                                                                                                                        ):
                                                                                                                            _gensym_2 = None
                                                                                                                        elif isinstance(
                                                                                                                                _gensym_51,
                                                                                                                                tuple
                                                                                                                        ):
                                                                                                                            if (len(
                                                                                                                                    _gensym_51
                                                                                                                            ) is 0
                                                                                                                                ):
                                                                                                                                _gensym_2 = (
                                                                                                                                )
                                                                                                                                (yield
                                                                                                                                 I
                                                                                                                                 .
                                                                                                                                 STORE_SUBSCR(
                                                                                                                                 )
                                                                                                                                 )
                                                                                                                            else:
                                                                                                                                _gensym_2 = None
                                                                                                                        else:
                                                                                                                            _gensym_2 = None
                                                                                                                        if (
                                                                                                                                _gensym_2
                                                                                                                                is
                                                                                                                                None
                                                                                                                        ):
                                                                                                                            _gensym_52 = sij.Call.__match__(
                                                                                                                                1,
                                                                                                                                _gensym_0
                                                                                                                            )
                                                                                                                            if (
                                                                                                                                    _gensym_52
                                                                                                                                    is
                                                                                                                                    None
                                                                                                                            ):
                                                                                                                                _gensym_2 = None
                                                                                                                            elif isinstance(
                                                                                                                                    _gensym_52,
                                                                                                                                    tuple
                                                                                                                            ):
                                                                                                                                if (len(
                                                                                                                                        _gensym_52
                                                                                                                                ) is 1
                                                                                                                                    ):
                                                                                                                                    _gensym_53 = _gensym_52[
                                                                                                                                        0]
                                                                                                                                    n = _gensym_53
                                                                                                                                    _gensym_2 = (
                                                                                                                                    )
                                                                                                                                    (yield
                                                                                                                                     I
                                                                                                                                     .
                                                                                                                                     CALL_FUNCTION(
                                                                                                                                         n
                                                                                                                                     )
                                                                                                                                     )
                                                                                                                                else:
                                                                                                                                    _gensym_2 = None
                                                                                                                            else:
                                                                                                                                _gensym_2 = None
                                                                                                                            if (
                                                                                                                                    _gensym_2
                                                                                                                                    is
                                                                                                                                    None
                                                                                                                            ):
                                                                                                                                _gensym_54 = sij.Print.__match__(
                                                                                                                                    0,
                                                                                                                                    _gensym_0
                                                                                                                                )
                                                                                                                                if (
                                                                                                                                        _gensym_54
                                                                                                                                        is
                                                                                                                                        None
                                                                                                                                ):
                                                                                                                                    _gensym_2 = None
                                                                                                                                elif isinstance(
                                                                                                                                        _gensym_54,
                                                                                                                                        tuple
                                                                                                                                ):
                                                                                                                                    if (len(
                                                                                                                                            _gensym_54
                                                                                                                                    ) is 0
                                                                                                                                        ):
                                                                                                                                        _gensym_2 = (
                                                                                                                                        )
                                                                                                                                        (yield
                                                                                                                                         I
                                                                                                                                         .
                                                                                                                                         PRINT_EXPR(
                                                                                                                                         )
                                                                                                                                         )
                                                                                                                                    else:
                                                                                                                                        _gensym_2 = None
                                                                                                                                else:
                                                                                                                                    _gensym_2 = None
                                                                                                                                if (
                                                                                                                                        _gensym_2
                                                                                                                                        is
                                                                                                                                        None
                                                                                                                                ):
                                                                                                                                    _gensym_55 = sij.BuildList.__match__(
                                                                                                                                        1,
                                                                                                                                        _gensym_0
                                                                                                                                    )
                                                                                                                                    if (
                                                                                                                                            _gensym_55
                                                                                                                                            is
                                                                                                                                            None
                                                                                                                                    ):
                                                                                                                                        _gensym_2 = None
                                                                                                                                    elif isinstance(
                                                                                                                                            _gensym_55,
                                                                                                                                            tuple
                                                                                                                                    ):
                                                                                                                                        if (len(
                                                                                                                                                _gensym_55
                                                                                                                                        ) is 1
                                                                                                                                            ):
                                                                                                                                            _gensym_56 = _gensym_55[
                                                                                                                                                0]
                                                                                                                                            n = _gensym_56
                                                                                                                                            _gensym_2 = (
                                                                                                                                            )
                                                                                                                                            (yield
                                                                                                                                             I
                                                                                                                                             .
                                                                                                                                             BUILD_LIST(
                                                                                                                                                 n
                                                                                                                                             )
                                                                                                                                             )
                                                                                                                                        else:
                                                                                                                                            _gensym_2 = None
                                                                                                                                    else:
                                                                                                                                        _gensym_2 = None
                                                                                                                                    if (
                                                                                                                                            _gensym_2
                                                                                                                                            is
                                                                                                                                            None
                                                                                                                                    ):
                                                                                                                                        _gensym_57 = sij.BuildTuple.__match__(
                                                                                                                                            1,
                                                                                                                                            _gensym_0
                                                                                                                                        )
                                                                                                                                        if (
                                                                                                                                                _gensym_57
                                                                                                                                                is
                                                                                                                                                None
                                                                                                                                        ):
                                                                                                                                            _gensym_2 = None
                                                                                                                                        elif isinstance(
                                                                                                                                                _gensym_57,
                                                                                                                                                tuple
                                                                                                                                        ):
                                                                                                                                            if (len(
                                                                                                                                                    _gensym_57
                                                                                                                                            ) is 1
                                                                                                                                                ):
                                                                                                                                                _gensym_58 = _gensym_57[
                                                                                                                                                    0]
                                                                                                                                                n = _gensym_58
                                                                                                                                                _gensym_2 = (
                                                                                                                                                )
                                                                                                                                                (yield
                                                                                                                                                 I
                                                                                                                                                 .
                                                                                                                                                 BUILD_TUPLE(
                                                                                                                                                     n
                                                                                                                                                 )
                                                                                                                                                 )
                                                                                                                                            else:
                                                                                                                                                _gensym_2 = None
                                                                                                                                        else:
                                                                                                                                            _gensym_2 = None
                                                                                                                                        if (
                                                                                                                                                _gensym_2
                                                                                                                                                is
                                                                                                                                                None
                                                                                                                                        ):
                                                                                                                                            _gensym_59 = sij.ListAppend.__match__(
                                                                                                                                                1,
                                                                                                                                                _gensym_0
                                                                                                                                            )
                                                                                                                                            if (
                                                                                                                                                    _gensym_59
                                                                                                                                                    is
                                                                                                                                                    None
                                                                                                                                            ):
                                                                                                                                                _gensym_2 = None
                                                                                                                                            elif isinstance(
                                                                                                                                                    _gensym_59,
                                                                                                                                                    tuple
                                                                                                                                            ):
                                                                                                                                                if (len(
                                                                                                                                                        _gensym_59
                                                                                                                                                ) is 1
                                                                                                                                                    ):
                                                                                                                                                    _gensym_60 = _gensym_59[
                                                                                                                                                        0]
                                                                                                                                                    n = _gensym_60
                                                                                                                                                    _gensym_2 = (
                                                                                                                                                    )
                                                                                                                                                    (yield
                                                                                                                                                     I
                                                                                                                                                     .
                                                                                                                                                     LIST_APPEND(
                                                                                                                                                         n
                                                                                                                                                     )
                                                                                                                                                     )
                                                                                                                                                else:
                                                                                                                                                    _gensym_2 = None
                                                                                                                                            else:
                                                                                                                                                _gensym_2 = None
                                                                                                                                            if (
                                                                                                                                                    _gensym_2
                                                                                                                                                    is
                                                                                                                                                    None
                                                                                                                                            ):
                                                                                                                                                _gensym_61 = sij.Return.__match__(
                                                                                                                                                    0,
                                                                                                                                                    _gensym_0
                                                                                                                                                )
                                                                                                                                                if (
                                                                                                                                                        _gensym_61
                                                                                                                                                        is
                                                                                                                                                        None
                                                                                                                                                ):
                                                                                                                                                    _gensym_2 = None
                                                                                                                                                elif isinstance(
                                                                                                                                                        _gensym_61,
                                                                                                                                                        tuple
                                                                                                                                                ):
                                                                                                                                                    if (len(
                                                                                                                                                            _gensym_61
                                                                                                                                                    ) is 0
                                                                                                                                                        ):
                                                                                                                                                        _gensym_2 = (
                                                                                                                                                        )
                                                                                                                                                        (yield
                                                                                                                                                         I
                                                                                                                                                         .
                                                                                                                                                         RETURN_VALUE(
                                                                                                                                                         )
                                                                                                                                                         )
                                                                                                                                                    else:
                                                                                                                                                        _gensym_2 = None
                                                                                                                                                else:
                                                                                                                                                    _gensym_2 = None
                                                                                                                                                if (
                                                                                                                                                        _gensym_2
                                                                                                                                                        is
                                                                                                                                                        None
                                                                                                                                                ):
                                                                                                                                                    _gensym_62 = sij.Defun.__match__(
                                                                                                                                                        6,
                                                                                                                                                        _gensym_0
                                                                                                                                                    )
                                                                                                                                                    if (
                                                                                                                                                            _gensym_62
                                                                                                                                                            is
                                                                                                                                                            None
                                                                                                                                                    ):
                                                                                                                                                        _gensym_2 = None
                                                                                                                                                    elif isinstance(
                                                                                                                                                            _gensym_62,
                                                                                                                                                            tuple
                                                                                                                                                    ):
                                                                                                                                                        if (len(
                                                                                                                                                                _gensym_62
                                                                                                                                                        ) is 6
                                                                                                                                                            ):
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                0]
                                                                                                                                                            doc = _gensym_63
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                1]
                                                                                                                                                            filename_ = _gensym_63
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                2]
                                                                                                                                                            frees = _gensym_63
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                3]
                                                                                                                                                            name = _gensym_63
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                4]
                                                                                                                                                            args = _gensym_63
                                                                                                                                                            _gensym_63 = _gensym_62[
                                                                                                                                                                5]
                                                                                                                                                            suite = _gensym_63
                                                                                                                                                            _gensym_2 = (
                                                                                                                                                            )
                                                                                                                                                            co_filename = (
                                                                                                                                                                filename_
                                                                                                                                                                or
                                                                                                                                                                filename
                                                                                                                                                            )
                                                                                                                                                            has_free = bool(
                                                                                                                                                                frees
                                                                                                                                                            )
                                                                                                                                                            if has_free:
                                                                                                                                                                for freevar in frees:
                                                                                                                                                                    (yield
                                                                                                                                                                     I
                                                                                                                                                                     .
                                                                                                                                                                     LOAD_CLOSURE(
                                                                                                                                                                         freevar
                                                                                                                                                                     )
                                                                                                                                                                     )
                                                                                                                                                                (yield
                                                                                                                                                                 I
                                                                                                                                                                 .
                                                                                                                                                                 BUILD_TUPLE(
                                                                                                                                                                     len(
                                                                                                                                                                         frees
                                                                                                                                                                     )
                                                                                                                                                                 )
                                                                                                                                                                 )
                                                                                                                                                            (
                                                                                                                                                                code,
                                                                                                                                                                loc_map
                                                                                                                                                            ) = self.lower(
                                                                                                                                                                name,
                                                                                                                                                                co_filename,
                                                                                                                                                                _line,
                                                                                                                                                                doc,
                                                                                                                                                                args,
                                                                                                                                                                frees,
                                                                                                                                                                suite
                                                                                                                                                            )
                                                                                                                                                            inner_frees.update(
                                                                                                                                                                code
                                                                                                                                                                .
                                                                                                                                                                co_freevars
                                                                                                                                                            )
                                                                                                                                                            loc_maps.append(
                                                                                                                                                                (code,
                                                                                                                                                                 loc_map
                                                                                                                                                                 )
                                                                                                                                                            )
                                                                                                                                                            (yield
                                                                                                                                                             I
                                                                                                                                                             .
                                                                                                                                                             LOAD_CONST(
                                                                                                                                                                 code
                                                                                                                                                             )
                                                                                                                                                             )
                                                                                                                                                            (yield
                                                                                                                                                             I
                                                                                                                                                             .
                                                                                                                                                             LOAD_CONST(
                                                                                                                                                                 name
                                                                                                                                                             )
                                                                                                                                                             )
                                                                                                                                                            (yield
                                                                                                                                                             I
                                                                                                                                                             .
                                                                                                                                                             MAKE_FUNCTION(
                                                                                                                                                                 has_free
                                                                                                                                                             )
                                                                                                                                                             )
                                                                                                                                                        else:
                                                                                                                                                            _gensym_2 = None
                                                                                                                                                    else:
                                                                                                                                                        _gensym_2 = None
                                                                                                                                                    if (
                                                                                                                                                            _gensym_2
                                                                                                                                                            is
                                                                                                                                                            None
                                                                                                                                                    ):
                                                                                                                                                        raise NotExhaustive

        code = bytec.Bytecode([set_lineno(instr) for instr in gen_instrs()])
        code.argnames.extend(args)
        code.filename = filename
        code.first_lineno = lineno
        code.docstring = doc
        code.name = name
        code.argcount = len(args)
        cellvars = set()
        for each in code:
            if (not isinstance(each, bytec.Instr)):
                continue
            if (not isinstance(each.arg, bytec.FreeVar)):
                continue
            varname = each.arg.name
            if (varname not in frees):
                each.arg = bytec.CellVar(varname)
                cellvars.add(varname)
        for varname in code.argnames:
            if (varname in frees):
                cellvars.add(varname)
        code.freevars = frees
        code.cellvars = list(cellvars)
        stacksize = code.compute_stacksize()
        ccode = resolve_blockaddr(code)
        ccode.flags = bytec.flags.infer_flags(ccode)
        pycode = ccode.to_code(stacksize)
        unmarshall_objs = {}
        consts = pycode.co_consts
        for (val_str, (is_unmarshal_obj, val_o)) in const_pool.items():
            if is_unmarshal_obj:
                unmarshall_objs[val_str] = consts.index(val_o)
                val_o.pop()
        nested_unmarshal_info = []
        for (code, loc_map) in loc_maps:
            nested_unmarshal_info.append((consts.index(code), loc_map))
        return (pycode, (unmarshall_objs, nested_unmarshal_info))
