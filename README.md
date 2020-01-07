
# sijuiacion-lang

[![Documentation Status](https://readthedocs.org/projects/sijuiacion-lang/badge/?version=latest)](https://sijuiacion-lang.readthedocs.io/en/latest/?badge=latest)
      
      
Sijuiacion, a.k.a "橘势", is a programming language to achieve a better use of
a subset of of the CPython bytecode instructions.

It provides some useful high level instructions, e.g, the Indirect Jumps,
and the Switch instructions, that are much more efficient than stacked if-else statements.

This idea is not originated by me, and I even just heard(got introduced about)
this from someone else. I must appreciate him for bringing me how to
use `END_FINALLY` to achieve this "fast switch" in Python.

# Installation

Clone this repo, and

```
pip install -U moshmosh-base --no-compile
cd sijuiacion-lang
pip install . --no-compile
```

# Usage

```
> cat x.sij

runtime operator
filename "x.sij"
firstlineno 3
const #add#
const #"hello "#
const #"sij"#
call 2
print
const #None#
return

> sij run xxx.sij
hello sij
> sij cc xxx.sij xxx.pyc && python xxx.pyc
hello sij
```

# Preview

お前も舞うか？

The instruction set is listed at https://github.com/RemuLang/sijuiacion-lang/blob/master/sijuiacion_lang/sijuiacion.gen .

If you cannot read that, you're not a target user.

There is no hack, but simple compiler stuffs.

## A Backend for A Subset of Instructions

Defined in `sij.rbnf`.

```python
from sijuiacion_lang.interface import load_sij

source = """
runtime sys
firstlineno 5
const #lambda x: x + 1#
const #2#
call 1
print
const #None#
return
"""

code = load_sij(source)
exec(code)
# => 3
```
