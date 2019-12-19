# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""

from sijuiacion_lang.parser_wrap import parse

print(parse("""
runtime sys
firstlineno 5
const #lambda x: x + 1#
print

"""))
      