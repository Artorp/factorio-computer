# Assembly quickstart

A quick rundown of the assembly language used for this machine

### Table of Contents
* [Registers](#registers)
* [Instruction overview](#instruction-overview)
  * [Notation](#notation)
  * [Basic instructions](#basic-instructions)
  * [Memory instructions](#memory-instructions)
    * [The stack](#the-stack)
  * [ALU instructions](#alu-instructions)
    * [Arithmetic](#arithmetic)
    * [Logical](#logical)
  * [Branch instructions](#branch-instructions)
* [Labels](#labels)
* [Definitions](#definitions)
* [Macros](#macros)


## Registers

There are 32 general purpose registers labelled **R0** through **R31**.

**PC** is a special register that contains the program counter. It is read-only and can only be written to by using a branching instruction (`B`, `BZ`, or `BN`), see below.

**SP** is a special register that contains the stack pointer. It is possible to read from and write to it, but in general it's faster to use the `PUSH` and `POP` registers. Reading with `LOAD R, [SP, 1]` is akin to peek().

The stack pointer should be initialized to the highest word address before use. See the stack section below.

## Instruction overview

### Notation

In the explanation, the operands are labelled:
```
OPCODE o1, o2, o3
```
and so on.

The `/` symbol is used to signify a choice between different operand types. The different operand types are in the table below.

Notation | Description
:---: | ---
I | Immediate value, 32 bit signed
R | Register
R/I | Register or immediate value
R/I/R,I | Register or immediate or both (comma separated)
R/L | Register or label

### Basic instructions

Instruction | Description | Example usage
--- | --- | ---
HLT | Stop the computer | `HLT`
NOP | No operation (skip a CPU cycle) | `NOP`
MOV R, R/I | o1 := o2<br>Note: Updates ALU flags | `MOV R0, 5`<br>`MOV R1, PC`
HLTG | Stop computer with success sound | `HLTG`
HLTB | Stop computer with error sound | `HLTB`

### Memory instructions

The computer has access to 256 words in memory, each storing a 32-bit signed integer.

Instruction | Description | Example usage
--- | --- | ---
STORE R/I, [R/I/R,I] | M[sum(o2)] := o1 | `STORE 5, [R5]`<br>`STORE R1, [R2, 5]`<br>`STORE PC, [0]`
LOAD R, [R/I/R,I] | o1 := M[sum(o2)] | `LOAD R1, [0]`<br>`LOAD R2, [R5, 0xff]`
PUSH R/I/L | M[SP] := o1, SP = SP - 1 | `PUSH 5`<br>`PUSH R2`<br>`PUSH some_label`
POP R | SP = SP + 1, R := M[SP] | `POP R0`
CMEM | Clear RAM and registers | `CMEM`
CREG | Clear registers | `CREG`
CRAM | Clear RAM | `CRAM`

#### The stack

The top of the stack is initially at the memory address in the stack pointer (`SP`). The stack grows "down" in memory, so pushing decreases the stack pointer, and popping increases it.

There is yet no stack overflow detection, should the stack overflow it will begin overwriting the RAM from the buttom up.

The stack pointer should be initialized to the desired last address before using the stack. For 256 words, it will be address 255, or 0xff. Example program:

```
MOV SP, 0xff
PUSH 5
PUSH 10
POP R0 ; R0 = 10
POP R1 ; R1 = 5
```

### ALU instructions

#### Arithmetic

Instruction | Description | Example usage
--- | --- | ---
ADD R, R/I, R/I | o1 := o2 + o3 | `ADD R1, R2, 10`
SUB R, R/I, R/I | o1 := o2 - o3 | `SUB R1, R1, R2`
INC R | o1 := o1 + 1 | `INC R5`
DEC R | o1 := o1 - 1 | `DEC R5`
MUL R, R/I, R/I | o1 := o2 * o3 | `MUL R1, 5, 10`
DIV R, R/I, R/I | o1 := o2 / o3<br>(rounded down) | `DIV R1, R5, 10`
POW R, R/I, R/I | o1 := o2^o3 | `POW R1, R2, R3`
MOD R, R/I, R/I | o1 := o2 % o3 | `MOD R1, 10, R8`

#### Logical

Instruction | Description | Example usage
--- | --- | ---
ASR R, R/I, R/I | o1 := o2 >> o3<br>(arithmetic shift) | `ASR R1, R2, R3`
LSL R, R/I, R/I | o1 := o2 << o3 | `LSL R1, R2, R3`
LSR R, R/I | o1 := o2 >> 1 | `LSR R1, R2`
ROL R, R/I | o1 := o2 binary rotated left once | `ROL R1, 0x100`
ROR R, R/I | o1 := o2 binary rotated right once | `ROR R1, R2`
NOT R, R/I | o1 := ~o2<br>o1 := o2 xor 0xffffffff | `NOT R1, R2`
AND R, R/I, R/I | o1 := o2 & o3 | `AND R1, 0b10, 0b11`
OR R, R/I, R/I | o1 := o2 | o3 | `OR R1, R2, R3`
XOR R, R/I, R/I | o1 := o2 xor o3 | `XOR R1, R2, R3`

### Branch instructions

Conditional branches are based on the ALU flags Z and N, which are set based on the last number to run through the ALU. Z means the result was 0, N means the result was negative, and the absense of any flag means the result was a positive non-zero number.

Instruction | Description | Example usage
--- | --- | ---
B R/L | Branch to label or register | `B some_label`<br>`B 1f`<br>`B R1`
BZ R/L | Branch if Z-flag set | `BZ some_label`
BN R/L | Branch if N-flag set | `BN some_label`
CMP R/I, R/I | Update ALU flags based on o1 - o2 | `CMP R1, R2`
TST R/I | Update ALU flags based on o1 | `TST R1`<br>`TST -1`

## Labels

A label is a destination for branch instructions. Internally the label is the absolute PC address, and it can be used as any other number. There are two kinds of labels, symbolic and numeric.

### Symbolic labels (global)

Symbolic labels are global in nature. They can only be defined once.

Example:

```
MOV R1, 10
B label
MOV R1, 5    ; This instruction will be skipped
label:
NOP
```

### Numeric labels (local)

Numeric labels are local. A label with a single digit 0-9 is considered a numeric label. They can be defined multiple times. When branching to a numeric label, the digit must be followed by a "f" (for forward) or "b" (for back).

Example:
```
1:
MOV R1, R2
B 1f
MOV R1, 5    ; This instruction will be skipped
1:
NOP
```

## Definitions

Definitions are a mapping from one keyword to another. Definitions are replaced during the pre-processing stage when compiling.

Syntax:

`#def <name> <to_replace>`

Example:
```
#def memory_size 0x100
#def MOV CMP
```

## Macros

Like definitions, macros are evaluated during the pre-processing stage. Macros can reduce repetitive code.

Syntax:
```
#macro <name> <number_of_parameters>
<lines_to_be_inserted>
#endm
```

Example:
```
#macro push_three 3
PUSH $0
PUSH $1
PUSH $2
#endm

push_three R1 R2 PC
```

See the macro demo (demo_macros.fal) for more examples.

