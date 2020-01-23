from rbnf.py_tools.unparse import Unparser
from urgent.codegen import MissingDict

from sijuiacion_lang import lowering, codegen
# from sijuiacion_lang.lowering import ast
import ast
ns = MissingDict(lambda _: '_gensym_' + str(len(ns)))


class Namer(ast.NodeVisitor):
    def visit_Name(self, n: ast.Name):
        if not n.id.isidentifier():
            n.id = ns[n.id]

ast = lowering.__ast__
Namer().visit(ast)
with open('../sijuiacion_lang/lowering.py.gen', 'w') as f:
    Unparser(ast, f)


ast = codegen.__ast__
Namer().visit(ast)
with open('../sijuiacion_lang/codegen.py.gen', 'w') as f:
    Unparser(ast, f)