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

All of [common-attributes](#Attributes) can be placed here, optional.


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

This is one of the advanced feature in sijuiacion comparing to the ordinary Python instruction. 

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


... 
  


 







 


