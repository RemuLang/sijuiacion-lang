# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:36:08 2019

@author: twshe
"""

from sijuiacion_lang.parser import *
from rbnf_rts.rts import Tokens, State, AST
from typing import Union, Tuple, List
from typing_extensions import Literal

__all__ = ['parse']
_parse = mk_parser()

Errors = Tuple[Literal[False], List[Tuple[int, str]]]
Parsed = Tuple[Literal[True], AST]


def parse(text: str, filename: str = "unknown") -> Union[Parsed, Errors]:
    tokens = list(run_lexer(filename, text))
    print(tokens)
    res = _parse(State(), Tokens(tokens))
    if res[0]:
        return res[1]
    msgs = []
    for each in res[1]:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno
        colno = token.colno
        msgs.append(f"Line {lineno}, column {colno}, {msg}")
    raise SyntaxError(f"Filename {filename}:\n" + "\n".join(msgs))