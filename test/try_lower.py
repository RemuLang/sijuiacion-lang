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

import dis

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
