from typing import Optional
from rbnf_rts.token import Token
from rbnf_rts.routine import LRCommaList
from rbnf_rts.rts import AST
from sijuiacion_lang.moshmosh_rts import NotExhaustive
from sijuiacion_lang.lowering import sij, Lower
from sijuiacion_lang.parser import lexicals


def match_token(_, to_match):
    return (to_match.value, )


Token.__match__ = match_token


class Codegen():
    def __init__(self):
        self.ID_t = lexicals['ID']
        self.PY_t = lexicals['PY']
        self.INT_t = lexicals['INT']
        self.STR_t = lexicals['STRING']
        self.cg: Optional[Lower] = None

    def start(self, n: AST):
        assert (n.tag == 'START')
        runtime = n.contents[2].value
        self.cg = Lower(__import__(runtime))
        self.lower = self.cg.lower
        attrs = n.contents[3]
        instrs = n.contents[(-2)]
        doc = ''
        filename = ''
        free = []
        name = '<unnamed>'
        args = []
        lineno = 0
        if (attrs.tag == 'Attrs'):
            for (attrname, attrvalue) in self.attrs(attrs):
                _gensym_64 = attrname
                if ('document' == _gensym_64):
                    _gensym_2 = ()
                    doc = attrvalue
                else:
                    _gensym_2 = None
                if (_gensym_2 is None):
                    if ('filename' == _gensym_64):
                        _gensym_2 = ()
                        filename = attrvalue
                    else:
                        _gensym_2 = None
                    if (_gensym_2 is None):
                        if ('free' == _gensym_64):
                            _gensym_2 = ()
                            free = attrvalue
                        else:
                            _gensym_2 = None
                        if (_gensym_2 is None):
                            if ('name' == _gensym_64):
                                _gensym_2 = ()
                                name = attrvalue
                            else:
                                _gensym_2 = None
                            if (_gensym_2 is None):
                                if ('args' == _gensym_64):
                                    _gensym_2 = ()
                                    args = attrvalue
                                else:
                                    _gensym_2 = None
                                if (_gensym_2 is None):
                                    if ('lineno' == _gensym_64):
                                        _gensym_2 = ()
                                        lineno = int(attrvalue)
                                    else:
                                        _gensym_2 = None
                                    if (_gensym_2 is None):
                                        _gensym_2 = ()
                                        raise TypeError(
                                            'invalid attribute {}'.format(
                                                attrname))
                                        if (_gensym_2 is None):
                                            raise NotExhaustive
        instrs = self.instrs(instrs)
        return self.lower(name, filename, lineno, doc, args, [], instrs)

    def instrs(self, n: AST):
        assert (n.tag == 'Instrs')
        _gensym_65 = n.contents
        if isinstance(_gensym_65, tuple):
            if (len(_gensym_65) is 1):
                _gensym_66 = _gensym_65[0]
                hd = _gensym_66
                _gensym_2 = ()
                return [self.instr(hd)]
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            if isinstance(_gensym_65, tuple):
                if (len(_gensym_65) is 2):
                    _gensym_67 = _gensym_65[0]
                    init = _gensym_67
                    _gensym_67 = _gensym_65[1]
                    end = _gensym_67
                    _gensym_2 = ()
                    res = self.instrs(init)
                    res.append(self.instr(end))
                    return res
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
            if (_gensym_2 is None):
                _gensym_2 = ()
                raise TypeError('unknown structure of instrs')
                if (_gensym_2 is None):
                    raise NotExhaustive

    def attr(self, n: AST):
        _gensym_68 = n.contents
        if isinstance(_gensym_68, tuple):
            if (len(_gensym_68) is 2):
                _gensym_69 = _gensym_68[0]
                _gensym_70 = Token.__match__(1, _gensym_69)
                if (_gensym_70 is None):
                    _gensym_2 = None
                elif isinstance(_gensym_70, tuple):
                    if (len(_gensym_70) is 1):
                        _gensym_71 = _gensym_70[0]
                        attrname = _gensym_71
                        _gensym_69 = _gensym_68[1]
                        a = _gensym_69
                        _gensym_2 = ()
                        if (attrname in ('document', 'filename', 'name')):
                            return (attrname, eval(a.value))
                        if (attrname in ('free', 'args')):
                            return (attrname, self.ids(a))
                        if (attrname == 'firstlineno'):
                            return ('lineno', int(a.value))
                        if _:
                            raise TypeError(
                                'unknown attribute {}'.format(attrname))
                    else:
                        _gensym_2 = None
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            _gensym_2 = ()
            raise TypeError('unknown attribute')
            if (_gensym_2 is None):
                raise NotExhaustive

    def attrs(self, n):
        _gensym_72 = n.contents
        if isinstance(_gensym_72, tuple):
            if (len(_gensym_72) is 1):
                _gensym_73 = _gensym_72[0]
                hd = _gensym_73
                _gensym_2 = ()
                (yield self.attr(hd))
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            if isinstance(_gensym_72, tuple):
                if (len(_gensym_72) is 2):
                    _gensym_74 = _gensym_72[0]
                    init = _gensym_74
                    _gensym_74 = _gensym_72[1]
                    end = _gensym_74
                    _gensym_2 = ()
                    (yield from self.attrs(init))
                    (yield self.attr(end))
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
            if (_gensym_2 is None):
                raise NotExhaustive

    def ids(self, n: AST):
        _gensym_75 = n.contents
        if isinstance(_gensym_75, tuple):
            if (len(_gensym_75) is 2):
                _gensym_76 = _gensym_75[0]
                _gensym_76 = _gensym_75[1]
                _gensym_2 = ()
                return []
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            if isinstance(_gensym_75, tuple):
                if (len(_gensym_75) is 3):
                    _gensym_77 = _gensym_75[0]
                    _gensym_77 = _gensym_75[1]
                    idlist = _gensym_77
                    _gensym_77 = _gensym_75[2]
                    _gensym_2 = ()
                    return self.idlist(idlist)
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
            if (_gensym_2 is None):
                raise NotExhaustive

    def idlist(self, n):
        _gensym_78 = n.contents
        if isinstance(_gensym_78, tuple):
            if (len(_gensym_78) is 1):
                _gensym_79 = _gensym_78[0]
                hd = _gensym_79
                _gensym_2 = ()
                return [hd.value]
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            if isinstance(_gensym_78, tuple):
                if (len(_gensym_78) is 2):
                    _gensym_80 = _gensym_78[0]
                    init = _gensym_80
                    _gensym_80 = _gensym_78[1]
                    end = _gensym_80
                    _gensym_2 = ()
                    res = self.idlist(init)
                    res.append(end.value)
                    return res
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
            if (_gensym_2 is None):
                raise NotExhaustive

    def jump_cases(self, n):
        for each in LRCommaList(n):
            [i, _, s] = each.contents
            if (self.INT_t is i.idint):
                (yield (int(i.value), s.value))
            else:
                (yield (None, s.value))

    def instr(self, n: AST):
        assert (n.tag == 'Instr')
        elts = n.contents
        _gensym_81 = elts
        if isinstance(_gensym_81, tuple):
            if (len(_gensym_81) is 2):
                _gensym_82 = _gensym_81[0]
                _gensym_83 = Token.__match__(1, _gensym_82)
                if (_gensym_83 is None):
                    _gensym_2 = None
                elif isinstance(_gensym_83, tuple):
                    if (len(_gensym_83) is 1):
                        _gensym_84 = _gensym_83[0]
                        instrname = _gensym_84
                        _gensym_82 = _gensym_81[1]
                        if isinstance(_gensym_82, Token):
                            tk = _gensym_82
                            _gensym_2 = ()
                            if (tk.idint == self.ID_t):
                                return {
                                    'load': sij.Load,
                                    'store': sij.Store,
                                    'deref': sij.Deref,
                                    'deref!': sij.RefSet,
                                    'goto': sij.Goto,
                                    'goto-if': sij.GotoEq,
                                    'goto-if-not': sij.GotoNEq,
                                    'label': sij.Label,
                                    'blockaddr': sij.BlockAddr
                                }[instrname](tk.value)
                            if (tk.idint == self.PY_t):
                                assert (instrname == 'const')
                                return sij.Extern(tk.value[1:(-1)])
                            if (tk.idint == self.INT_t):
                                return {
                                    'rot': sij.ROT,
                                    'dup': sij.DUP,
                                    'list': sij.BuildList,
                                    'tuple': sij.BuildTuple,
                                    'line': sij.Line,
                                    'call': sij.Call
                                }[instrname](int(tk.value))
                            if _:
                                raise TypeError(
                                    'invalid instruction {}'.format(instrname))
                        else:
                            _gensym_2 = None
                    else:
                        _gensym_2 = None
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
        else:
            _gensym_2 = None
        if (_gensym_2 is None):
            if isinstance(_gensym_81, tuple):
                if (len(_gensym_81) is 1):
                    _gensym_85 = _gensym_81[0]
                    _gensym_86 = Token.__match__(1, _gensym_85)
                    if (_gensym_86 is None):
                        _gensym_2 = None
                    elif isinstance(_gensym_86, tuple):
                        if (len(_gensym_86) is 1):
                            _gensym_87 = _gensym_86[0]
                            single_instr = _gensym_87
                            _gensym_2 = ()
                            return {
                                'prj': sij.Item,
                                'prj!': sij.ItemSet,
                                'pop': sij.Pop,
                                'print': sij.Print,
                                'return': sij.Return,
                                'indir': sij.Indir
                            }[single_instr]()
                        else:
                            _gensym_2 = None
                    else:
                        _gensym_2 = None
                else:
                    _gensym_2 = None
            else:
                _gensym_2 = None
            if (_gensym_2 is None):
                if isinstance(_gensym_81, tuple):
                    if (len(_gensym_81) >= 1):
                        _gensym_88 = _gensym_81[0]
                        _gensym_89 = Token.__match__(1, _gensym_88)
                        if (_gensym_89 is None):
                            _gensym_2 = None
                        elif isinstance(_gensym_89, tuple):
                            if (len(_gensym_89) is 1):
                                _gensym_90 = _gensym_89[0]
                                if ('switch' == _gensym_90):
                                    _gensym_88 = _gensym_81[1:None]
                                    args = _gensym_88
                                    _gensym_2 = ()
                                    table = dict(self.jump_cases(args[(-1)]))
                                    return sij.Switch(table)
                                else:
                                    _gensym_2 = None
                            else:
                                _gensym_2 = None
                        else:
                            _gensym_2 = None
                    else:
                        _gensym_2 = None
                else:
                    _gensym_2 = None
                if (_gensym_2 is None):
                    if isinstance(_gensym_81, tuple):
                        if (len(_gensym_81) >= 1):
                            _gensym_91 = _gensym_81[0]
                            _gensym_92 = Token.__match__(1, _gensym_91)
                            if (_gensym_92 is None):
                                _gensym_2 = None
                            elif isinstance(_gensym_92, tuple):
                                if (len(_gensym_92) is 1):
                                    _gensym_93 = _gensym_92[0]
                                    if ('defun' == _gensym_93):
                                        _gensym_91 = _gensym_81[1:None]
                                        xs = _gensym_91
                                        _gensym_2 = ()
                                        doc = ''
                                        filename = ''
                                        free = []
                                        name = '<unnamed>'
                                        args = []
                                        _gensym_94 = xs
                                        if isinstance(_gensym_94, tuple):
                                            if (len(_gensym_94) is 3):
                                                _gensym_95 = _gensym_94[0]
                                                _gensym_95 = _gensym_94[1]
                                                instrs = _gensym_95
                                                _gensym_95 = _gensym_94[2]
                                                _gensym_2 = ()
                                                return sij.Defun(
                                                    doc, filename, free, name,
                                                    args, self.instrs(instrs))
                                            else:
                                                _gensym_2 = None
                                        else:
                                            _gensym_2 = None
                                        if (_gensym_2 is None):
                                            if isinstance(_gensym_94, tuple):
                                                if (len(_gensym_94) is 4):
                                                    _gensym_96 = _gensym_94[0]
                                                    attrs = _gensym_96
                                                    _gensym_96 = _gensym_94[1]
                                                    _gensym_96 = _gensym_94[2]
                                                    instrs = _gensym_96
                                                    _gensym_96 = _gensym_94[3]
                                                    _gensym_2 = ()
                                                    instrs = self.instrs(
                                                        instrs)
                                                    for (
                                                            attrname, attrvalue
                                                    ) in self.attrs(attrs):
                                                        _gensym_97 = attrname
                                                        if ('document' ==
                                                                _gensym_97):
                                                            _gensym_2 = ()
                                                            doc = attrvalue
                                                        else:
                                                            _gensym_2 = None
                                                        if (_gensym_2 is None):
                                                            if ('filename' ==
                                                                    _gensym_97
                                                                ):
                                                                _gensym_2 = ()
                                                                filename = attrvalue
                                                            else:
                                                                _gensym_2 = None
                                                            if (_gensym_2 is
                                                                    None):
                                                                if ('free' ==
                                                                        _gensym_97
                                                                    ):
                                                                    _gensym_2 = (
                                                                    )
                                                                    free = attrvalue
                                                                else:
                                                                    _gensym_2 = None
                                                                if (_gensym_2
                                                                        is
                                                                        None):
                                                                    if ('name'
                                                                            ==
                                                                            _gensym_97
                                                                        ):
                                                                        _gensym_2 = (
                                                                        )
                                                                        name = attrvalue
                                                                    else:
                                                                        _gensym_2 = None
                                                                    if (_gensym_2
                                                                            is
                                                                            None
                                                                        ):
                                                                        if ('args'
                                                                                ==
                                                                                _gensym_97
                                                                            ):
                                                                            _gensym_2 = (
                                                                            )
                                                                            args = attrvalue
                                                                        else:
                                                                            _gensym_2 = None
                                                                        if (_gensym_2
                                                                                is
                                                                                None
                                                                            ):
                                                                            if (
                                                                                    'lineno'
                                                                                    ==
                                                                                    _gensym_97
                                                                            ):
                                                                                _gensym_2 = (
                                                                                )
                                                                                instrs = [
                                                                                    sij
                                                                                    .
                                                                                    Line(
                                                                                        attrvalue
                                                                                    ),
                                                                                    *instrs
                                                                                ]
                                                                            else:
                                                                                _gensym_2 = None
                                                                            if (
                                                                                    _gensym_2
                                                                                    is
                                                                                    None
                                                                            ):
                                                                                _gensym_2 = (
                                                                                )
                                                                                raise TypeError(
                                                                                    'invalid attribute {}'
                                                                                    .
                                                                                    format(
                                                                                        attrname
                                                                                    )
                                                                                )
                                                                                if (
                                                                                        _gensym_2
                                                                                        is
                                                                                        None
                                                                                ):
                                                                                    raise NotExhaustive
                                                    return sij.Defun(
                                                        doc, filename, free,
                                                        name, args, instrs)
                                                else:
                                                    _gensym_2 = None
                                            else:
                                                _gensym_2 = None
                                            if (_gensym_2 is None):
                                                _gensym_2 = ()
                                                raise TypeError(
                                                    'invalid args for defun, seems impossible'
                                                )
                                                if (_gensym_2 is None):
                                                    raise NotExhaustive
                                    else:
                                        _gensym_2 = None
                                else:
                                    _gensym_2 = None
                            else:
                                _gensym_2 = None
                        else:
                            _gensym_2 = None
                    else:
                        _gensym_2 = None
                    if (_gensym_2 is None):
                        raise NotExhaustive
