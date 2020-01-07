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
runtime numpy     
filename "play-with-numpy.sij"
firstlineno 3

const #10#
switch
  | 10 => a
  | _  => b

label a
const #"jump to a"#
print
goto end

label b
const #"jump to b"#
print
goto end

label end

const #10#
return
"""

mk = load_sij(src)
# dis.dis(mk.co_consts[2][0])
dumps(mk)
exec(mk)
