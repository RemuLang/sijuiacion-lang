# Get Started

## Introduction

Sijuiacion is a programming language based on CPython Virtual Machine.

It provides the flexibility of working with CPython VM for various purpose.

The motivating use case of this is on the fly making compiler backends,
and further, the expert skills encoded in this project also enables the infrastructures for creating following advanced language constructs/features based on Python,

- stackless-coroutine, indirect jump/label as value,
- switch/pattern matching,
- generalised constants(instead of merely objects accepted by CPython `marshal.dumps`), etc.

Also, the sijuiacion compiler will generate standalone `.pyc` file,
which is convenient for distribution.

About the ecosystem, either embedding Python or being embedded in Python is natural and, trivial.

## Installation

```shell
pip install -U moshmosh-base --no-compile
git clone https://github.com/RemuLang/sijuiacion-lang
cd sijuiacion-lang
pip install . --no-compile
```

Then you can use the command `sij run` or `sij cc`,
by which can one run or compile(to `.pyc`) sijuiacion source code.


## Basic Example

Create a file called `hw.sij`, filling

```sijuiacion
runtime operator
filename "switch.sij"
firstlineno 3

const #add#
const #"hello "#
const #"sijuiacion!"#
call 2
print

const #None#
return
```

You're expected to get
```shell
ushell> sij cc hw.sij hw.pyc && python hw.pyc # or `sij run hw.sij`
'hello sijuiacion!'
```

`print` instruction corresponds to Python's `PRINT_EXPR`. You can refer to the documentation [dis](https://docs.python.org/3/library/dis.html).

## Variables

Local variables can be manipulated by `load` and `store` instructions.

```sijuiacion
runtime operator
filename "switch.sij"
firstlineno 3

const #add#
store add
load add
print

const #None#
return
```
produces
```
<built-in function add>
```


## Functions

```sijuiacion
runtime operator
filename "switch.sij"
firstlineno 3

defun
    args [x y]
    {
        line 7

        load x
        load y
        tuple 2
        return 
    }
const #mul#
const #6#

call 2
print

const #None#
return
```
outputs
```
(<built-in function mul>, 6)
```

## Closures, and sharing variables

Unlike languages with advanced scope constructs, in Python VM,
only functions create their own scopes.

There're 2 kinds of sharing variables in Python, the first of which is called **free variables**, and they're made in outer scopes.

Another sort of variables are the **cell variables**.

For each scope/function, its cell variables must be bounded in this current scope,
but referenced by its inner scopes.

Within sijuiacion, you just need to specify free variables when creating functions,
by adding an attribute to the function definition: for example, `free [var1 var2 var3]`.

Besides, accessing or mutating the free/cells variables requires the instruction `deref` or `deref!`, respectively.

```sijuiacion
runtime operator
filename "switch.sij"
firstlineno 3

const #1#
deref! y

defun
    free [y]
    args [x]
    {
        line 7

        load x
        deref y
        tuple 2
        return 
    }
const #mul#
call 1
print

const #None#
return
```

outputs

```
(<built-in function mul>, 1)
```
