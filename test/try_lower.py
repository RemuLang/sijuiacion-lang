from sijuiacion_lang.lowering import sij, Lower

lowerer = Lower(env={})


def mk_code(label):
    assert label in 'abcd'
    return lowerer.lower("name", "fname", 1, "no doc", [], [], [
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
exec(mk_code("a")[0])

print("b".center(20, '='))
exec(mk_code("b")[0])

print("c".center(20, '='))
exec(mk_code("c")[0])

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


code, _ = lowerer.lower("name", "fname", 1, "no doc", ["x"], [], [
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
    sij.Extern("114514"),
    sij.Print(),
    sij.Label("d"),
    # sij.Glob("Exception"),
    # sij.Const("haha"),
    # sij.Call(1),
    # sij.SimpleRaise(),
    sij.Const(None),
    sij.Return()
])
f.__code__ = code

print("input=11".center(20, '='))
f(11)

print("input=45".center(20, '='))
f(45)

"""
======input=11======
6
7
114514
======input=45======
7
114514
"""