# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:39 2019

@author: twshe
"""
import dis

from sijuiacion_lang.interface import load_sij
from pathlib import Path

for p in Path('sij-scripts').iterdir():
    if p.suffix.endswith('sij'):
        # if p.name =='switch.sij':
        try:
            with p.open() as f:
                mk = load_sij(f.read())
            # dis.dis(mk.co_consts[2][0])
            exec(mk)
        except:
            print(p)
            raise
