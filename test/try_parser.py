# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
import dis

from sijuiacion_lang.parser_wrap import parse
from sijuiacion_lang.codegen import Codegen
from sijuiacion_lang.interface import load_sij
from marshal import dumps
import bytecode as bytec

cg = Codegen()
# ast = parse("""
# runtime sys
# firstlineno 5
# const #lambda x: x + 1#
# const #2#
# call 1
# return
# """)
#
# code = cg.start(ast)
# assert eval(code) == 3

src = """
runtime operator
filename "switch.sij"
firstlineno 3

const #1#
deref! y

defun
    free [y]
    args [x]
    {
        line 7

        load x
        deref y
        tuple 2
        return 
    }
const #mul#
call 1
print

const #None#
return
"""

mk = load_sij(src)
# dis.dis(mk.co_consts[2][0])
dumps(mk)
exec(mk)
