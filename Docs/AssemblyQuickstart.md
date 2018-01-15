# Assembly quickstart

A quick rundown of the assembly language used for this machine

# Registers

There are 32 general purpose registers labelled R0 through R31.

PC is a special register that contains the program counter. It is read-only and can only be written to by using a branching instruction (`B`, `BZ`, or `BN`), see below.

# Instruction overview

## Notation

I = Immediate value, 32 bit signed

R = Register

R/I = Register or immediate value

R/I/R, I = Register or immediate or both (comma separated)

R/L = Register or label

## Basic instructions

Instruction | Description | Example usage

## Memory instructions

## Arithmetic and logic instructions

## Branch instructions

# Labels

## Symbolic labels (global)

## Numeric labels (local)

# Definitions

`#def <from> <to>`

# Macros

`#macro <name> <number_of_parameters>`

`#mend`
