# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
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
filename "nested-functions.sij"
firstlineno 3


defun
    {
        const #1#
        store x
        defun
            free [x]{
                deref x
                return
            }
        call 0
        return
    }

call 0
print

const #0#
return
"""

mk = load_sij(src)
dumps(mk)
exec(mk)
