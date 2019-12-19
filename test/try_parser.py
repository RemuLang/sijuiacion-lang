# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
from sijuiacion_lang.parser_wrap import parse
from sijuiacion_lang.codegen import Codegen

ast = parse("""
runtime sys
firstlineno 5
const #lambda x: x + 1#
const #2#
call 1
print
const #None#
return
""")

cg = Codegen()
code = cg.start(ast)
exec(code)

      