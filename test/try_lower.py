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
