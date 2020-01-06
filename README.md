# sijuiacion-lang

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
from sijuiacion_lang.parser_wrap import parse
from sijuiacion_lang.codegen import Codegen
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


## Python APIs

```python
from sijuiacion_lang.lowering import *


def mk_code(label):
    assert label in 'abcd'
    return lower(
    "name",
    "fname",
    1,
    "no doc",
    [],
    [
        sij.BlockAddr(label),
        sij.Indir(),
        sij.Const(5),
        sij.Print(),
        sij.Label("a"),
        sij.Const(6),
        sij.Print(),
        sij.Label("b"),
        sij.Const(7),
        sij.Print(),
        sij.Label("c"),
        sij.Const(8),
        sij.Print(),
        sij.Label("d"),
        sij.Const(None),
        sij.Return(),
    ])

print("a".center(20, '='))
exec(mk_code("a"))

print("b".center(20, '='))
exec(mk_code("b"))

print("c".center(20, '='))
exec(mk_code("c"))


# Output:
# =========a==========
# 6
# 7
# 8
# =========b==========
# 7
# 8
# =========c==========
# 8

def f(x):
    pass
code = lower(
"name",
"fname",
1,
"no doc",
["x"],
[
    sij.Load("x"),
    sij.Switch({
        11: "a",
        45: "b",
        14: "c",
        0: "d"
    }),
    sij.Const(5),
    sij.Print(),
    sij.Label("a"),
    sij.Const(6),
    sij.Print(),
    sij.Label("b"),
    sij.Const(7),
    sij.Print(),
    sij.Label("c"),
    sij.Const(8),
    sij.Print(),
    sij.Label("d"),
    sij.Const(None),
    sij.Return(),
])
f.__code__ = code


print("input=11".center(20, '='))
f(11)

print("input=45".center(20, '='))
f(45)

# ======input=11======
# 6
# 7
# 8
# ======input=45======
# 7
# 8
```