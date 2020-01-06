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
firstlineno 5
defun
  args [x]
  {
  const #add#
  const #1#
  load x
  call 2
  return
}
const #8#
call 1
print
const #None#
return
"""

mk = load_sij(src)
dumps(mk)
exec(mk)
