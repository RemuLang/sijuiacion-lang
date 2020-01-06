# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
from sijuiacion_lang.parser_wrap import parse
from sijuiacion_lang.codegen import Codegen
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

ast = parse("""
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
return
""")

code, info = cg.start(ast)


def mk_code():
    runtime = __import__("runtime").__dict__
    code, info = "code"

    def nest(code, info):
        co_consts = code.co_consts
        for eval_str, index in info[0].items():
            co_consts[index].append(eval(eval_str, runtime))
        for index, nest_info in info[1]:
            nest(co_consts[index], nest_info)

    nest(code, info)
    exec(code)


mk = bytec.Bytecode.from_code(mk_code.__code__)
const_map = {"runtime": cg.cg.env.__name__, 'code': (code, info)}

for each in mk:
    if isinstance(each, bytec.Instr):
        if each.name == 'LOAD_CONST':
            arg = const_map.get(each.arg)
            if arg:
                each.arg = arg
mk = mk.to_code()
exec(mk)
