# moshmosh?
# +pattern-matching
from typing import Optional
from rbnf_rts.token import Token
from rbnf_rts.rts import AST
from sijuiacion_lang.lowering import sij, Lower
from sijuiacion_lang.parser import lexicals


def match_token(_, to_match):
    return to_match.value,


Token.__match__ = match_token


class Codegen:

    def __init__(self):
        self.ID_t = lexicals['ID']
        self.PY_t = lexicals['PY']
        self.INT_t = lexicals['INT']
        self.STR_t = lexicals['STRING']
        self.cg: Optional[Lower] = None

    def start(self, n: AST):
        assert n.tag == "START"
        runtime = n.contents[2].value
        self.cg = Lower(__import__(runtime))
        self.lower = self.cg.lower

        attrs = n.contents[3]
        instrs = n.contents[-2]
        doc = ""
        filename = ""
        free = []
        name = "<unnamed>"
        args = []
        lineno = 0
        if attrs.tag == "Attrs":
            for attrname, attrvalue in self.attrs(attrs):
                with match(attrname):
                    if "document":
                        doc = attrvalue
                    if "filename":
                        filename = attrvalue
                    if "free":
                        free = attrvalue
                    if "name":
                        name = attrvalue
                    if "args":
                        args = attrvalue
                    if "lineno":
                        lineno = int(attrvalue)
                    if _:
                        raise TypeError("invalid attribute {}".format(attrname))
        instrs = self.instrs(instrs)
        return self.lower(name, filename, lineno, doc, args, instrs)

    def instrs(self, n: AST):
        assert n.tag == "Instrs"
        with match(n.contents):
            if (hd,):
                return [self.instr(hd)]
            if (init, end):
                res = self.instrs(init)
                res.append(self.instr(end))
                return res
            if _:
                raise TypeError("unknown structure of instrs")

    def attr(self, n: AST):
        with match(n.contents):
            if (Token(attrname), a):
                if attrname in ('document', 'filename', 'name'):
                    return attrname, eval(a.value)
                if attrname in ('free', 'args'):
                    return attrname, self.ids(a)
                if attrname == 'firstlineno':
                    return 'lineno', int(a.value)
                if _:
                    raise TypeError("unknown attribute {}".format(attrname))
            if _:
                raise TypeError("unknown attribute")

    def attrs(self, n):
        with match(n.contents):
            if (hd,):
                yield self.attr(hd)
            if (init, end):
                yield from self.attrs(init)
                yield self.attr(end)

    def ids(self, n: AST):
        with match(n.contents):
            if (_, _):
                return []
            if (_, idlist, _):
                return self.idlist(idlist)

    def idlist(self, n):
        with match(n.contents):
            if (hd,):
                return [hd.value]
            if (init, end):
                res = self.idlist(init)
                res.append(hd.value)
                return res

    def instr(self, n: AST):
        assert n.tag == "Instr"
        elts = n.contents
        with match(elts):
            if (Token(instrname), isinstance(Token) and tk):
                if tk.idint == self.ID_t:
                    return {
                        'load': sij.Load, 'store': sij.Store, 'deref': sij.Deref, 'deref!': sij.RefSet,
                        'goto': sij.Goto, 'goto-if': sij.GotoEq, 'goto-if-not': sij.GotoNEq, 'label': sij.Label
                    }[instrname](tk.value)
                if tk.idint == self.PY_t:
                    assert instrname == "const"
                    return sij.Const(tk.value[1:-1])
                if tk.idint == self.INT_t:
                    return {
                        'rot': sij.ROT, 'dup': sij.DUP, 'list': sij.BuildList, 'tuple': sij.BuildTuple,
                        'line': sij.Line, 'call': sij.Call
                    }[instrname](int(tk.value))
                if _:
                    raise TypeError("invalid instruction {}".format(instrname))
            if (Token("prj"),):
                return sij.Item()
            if (Token("prj!"),):
                return sij.ItemSet()
            if (Token("pop"),):
                return sij.Pop()
            if (Token("print"),):
                return sij.Print()
            if (Token("return"),):
                return sij.Return()
            if (Token("defun"), *xs):
                doc = ""
                filename = ""
                free = []
                name = "<unnamed>"
                args = []
                with match(xs):
                    if (_, instrs, _):
                        return sij.Defun(doc, filename, free, name, args, self.instrs(instrs))
                    if (attrs, _, instrs, _):
                        instrs = self.instrs(instrs)
                        for attrname, attrvalue in self.attrs(attrs):
                            with match(attrname):
                                if "document":
                                    doc = attrvalue
                                if "filename":
                                    filename = attrvalue
                                if "free":
                                    free = attrvalue
                                if "name":
                                    name = attrvalue
                                if "args":
                                    args = attrvalue
                                if "lineno":
                                    instrs = [sij.Line(attrvalue), *instrs]
                                if _:
                                    raise TypeError("invalid attribute {}".format(attrname))
                        return sij.Defun(doc, filename, free, name, args, instrs)
                    if _:
                        raise TypeError("invalid args for defun, seems impossible")
