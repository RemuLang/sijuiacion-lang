# Sijuiacion Instructions and Attributes

## Instruction Grammar

The language of sijuiacion is pretty small, we can check its BNF notations.

(Note that this BNF notation is introduced by me, called [RBNF](https://github.com/thautwarm/RBNF.hs).
 
```rbnf
START : <BOF>
        'runtime' <ID> [Attrs] Instrs
        <EOF>
        ;

Instrs : [Instrs] Instr;

Instr : 'load'   <ID>
      | 'store'  <ID>
      | 'deref'  <ID>
      | 'deref!' <ID>
      | 'const'  <PY>

      | 'print'
      | 'pop'
      | 'prj'
      | 'prj!'
      | 'indir'

      | 'rot'    <INT>
      | 'dup'    <INT>
      | 'goto'   <ID>
      | 'goto-if'     <ID>
      | 'goto-if-not' <ID>
      | 'label'       <ID>
      | 'blockaddr'   <ID>

      | 'call'        <INT>
      | 'list'        <INT>
      | 'tuple'       <INT>
      | 'return'
      | 'line'        <INT>
      | 'defun' [Attrs] '{' Instrs '}'
      | 'switch' ['|'] JumpCases
      ;

JumpCase : <INT> '=>' <ID>;
JumpCase : '_' '=>' <ID>;

JumpCases : [JumpCases '|'] JumpCase;

Attrs : [Attrs] Attr;

Attr : 'document' <STRING>
     | 'filename' <STRING>
     | 'free' IDs
     | 'name' <STRING>
     | 'args' IDs
     | 'firstlineno' <INT>
     ;

IDs : '[' [IDList] ']';
IDList : [IDList] <ID>;
```

## Entry Attributes 
### `runtime` attributes

This is mandatory, placed in the head of file, followed by an identifier.

The trailing identifier refers to a Python module, whose global variables can be leveraged to construct the operand of `const` instruction.

For instance,
```sijuiacion
runtime operator
...
const #add#
```

In `#add#`, the expression `add` is evaluated in the global scope of module `operator`.

### Optional attributes

Some of [these attributes](#Attributes) can be placed here, all optional.

Attributes `free` and `args` are not allowed in the entry of the file.


## Instruction

### `load`

Followed by an identifier indicating local variable name,
and put the accessed object on the top of stack(TOS).
 
Basically, it's `LOAD_FAST` in CPython VM.
 
### `store`

Followed by an identifier indicating local variable name,
and store(consumed) TOS as the variable.

Basically, it's `STORE_FAST` in Python VM.

### `deref`

Similar to `load`, but works for cell variables and free variables.

Basically, `LOAD_DEREF` in Python VM.

### `deref!`

Similar to `store`,  but works for cell variables and free variables.

Basically, `STORE_DEREF` in Python VM.

### `const`

Followed by a python expression surrounded by `#`, e.g., `const #value#`.

Basically, `LOAD_CONST` in Python VM.

However, when the operand is not serializable with Python's `marshal` stand library,
by some interesting strategy I came up with, it'll be linked later, the produced CPython instructions are:
```
LOAD_CONST [<object linked later>]
LOAD_CONST 0
BINARY_SUBSCR
```

### `print`

`PRINT_EXPR` in Python VM.

### `pop`

`POP_TOP` in Python VM.

### `prj`

Named after the term "Projection".

`BINARY_SUBSCR` in Python VM.

The semantics can be demonstrated using Python code:

```python
key = stack.pop()
base = stack.pop()
stack.append(base[key])
```


### `prj!`

Named after the term "Projection".

`STORE_SUBSCR` in Python VM.

The semantics can be demonstrated using Python code:

```python
value = stack.pop()
key = stack.pop()
base = stack.pop()
base[key] = value
```

### `indir`

This is one of the advanced features in sijuiacion comparing to the ordinary Python instruction. 

It consumes the TOS, and jump to the corresponding offset of current frame.

You're supposed to use this with `blockaddr`, or your program will be vulnerable,
because you cannot know where you're jumping.    

A valid example is:

```sijuiacion
blockaddr a
indir
...
label a
```

Comparing to `goto`, `indir` and `blockaddr` make the label **first-class**.

### `blockaddr`

Followed by a name of a label in current frame,
and place the resolved label offset as an integer as TOS.

This is the most precious part of this project, which further enables the feature of **label as value**,
and the form of instructions like `switch`.

A valid code for this, showing we can pass the block address outside current frame.

```sijuiacion
blockaddr a
return
```

### `goto`

Followed by the name of a label, to which directly jumps.

### `label`

Followed by an identifier, declaring a point that can be jumped to.

### `call`

For instance,  `call 2` can be demonstrated with Python code:
```python
arg2 = stack.pop()
arg1 = stack.pop()
f = stack.pop()
stack.append(f(arg1, arg2))
```

### `return`

Return TOS for current function.

### `line`

Followed by an integer, setting metadata, and when runtime error occurs,
point to the correct line number.

P.S: Another important metadata attribute for runtime error reporting is `filename`.

### `dup`

Followed by an integer which means how many times to duplicate TOS.


### `goto-if`

Followed by the name of a label name, to which jump if `TOS` is true. TOS consumed.

### `goto-if-not`

Followed by the name of a label name, to which jump if `TOS` is false. TOS consumed.

### `rot`

Can only be followed by `2` or `3`, equivalent to Python instruction `ROT_TWO` or `ROT_THREE`, respectively.

P.S: `ROT_FOUR` is added to Python instruction set, thus, this is going to get supported.

### `list`

Followed by an integer, hereafter as `N`, then build a Python list by consuming the top `N` elements.

We use python code to demonstrate the semantics of `list 2`:

```python
elt2 = stack.pop()
elt1 = stack.pop()
stack.append([elt1, elt2])
```

### `tuple`

Similar to `list` but build a tuple.

### `switch`

For instance,
```sijuiacion
switch
| 1 => a
| _ => b
```
You can read it as "take TOS(consumed), if TOS equals to 1, jump to label a; otherwise, jump to label b".

`_ => b` is a default case.

P.S:

1. Holding multiple cases is allowed, and no default case is permitted.
2. The first `|` can be omitted.


### `defun`

Define a function and place it as TOS.

Firstly, followed by a series of [attributes](#Attributes), where all of those kinds of attributes are allowed here.

Then, followed by a series of instructions enclosed by `{` and `}`.

For instance,

```sijuiacion
defun {
    const #0#
    return
}
call 0

defun args [x] {
    load x
    return x
}
const #1#
call 1

const #2#
deref! a
defun free [a] {
    deref a
    return
}
call 0

tuple 3
print
```

produces `(0, 1, 2)`.

## Attributes

### `document`

Followed by a double-quoted string, representing the documentation of the code object.

### `filename`

Followed by a double-quoted string, representing the definition filename of the code object.

### `free`

Followed by a non-separated list of identifiers, representing the free variables of the code object.

**NOTE**: `defun` only, cannot be used in file entry.

### `args`

Followed by a non-separated list of identifiers, representing the arguments of the code object.

For simplifying our language, only positional arguments are permitted.

Further, you can create helper functions in Python side to access a fuller set of function call functionalities.

**NOTE**: `defun` only, cannot be used in file entry.

### `name`

Followed by a double-quoted string, representing the name of the code object.

### `firstlineno`

Followed by a double-quoted string, representing the first line number of the code object.
