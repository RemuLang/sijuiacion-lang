from Redy.Opt import feature, constexpr
import timeit


class Closure(tuple):
    def __call__(self, a):
        c, f = self
        return f(c, a)


def f1(x):
    def g(y):
        return x + y

    return g


def fc(c, y):
    return c + y


@feature(constexpr)
def f2(x):
    return constexpr[Closure]((x, constexpr[fc]))


print(f1(1)(2))
print(f2(1)(2))
# 3
# 3

# mk closure
print(timeit.timeit("f(1)", globals=dict(f=f1)))
print(timeit.timeit("f(1)", globals=dict(f=f2)))
# 0.15244655999958923
# 0.16590227899905585

f1_ = f1(2)
f2_ = f2(2)
print(timeit.timeit("f(1)", globals=dict(f=f1_)))
print(timeit.timeit("f(1)", globals=dict(f=f2_)))

# 0.08070355000018026
# 0.20936105600048904

# So, use builtin closures instead of making our own
