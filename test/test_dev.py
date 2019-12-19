# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:57:40 2019

@author: twshe
"""

from sijuiacion_lang.lowering import sij, lower


code = lower(
  "mod",
  "f.txt",
  1,
  "aa",
  [],
  [
       
       sij.Defun("hh",
                 "f.txt",
                 [], 
                 "lam",
                 ["y"],
                 [
                   sij.Const(lambda x, y: x + y),
                   sij.Const(1),
                   sij.Load("y"),
                   sij.Return()
                 ]),
        sij.DUP(1),
        sij.Print(),
        sij.Const(2),
        sij.Call(1),
        sij.Print(),
        sij.Const(None),
        sij.Return()
  ]
)
exec(code)