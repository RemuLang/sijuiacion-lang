# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
from sijuiacion_lang.interface import load_sij
with open("sij-scripts/stack-less.sij") as f:
    mk = load_sij(f.read())

exec(mk)
