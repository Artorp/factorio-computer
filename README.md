# factorio-computer

A programmable general-purpose computer built in Factorio. It comes with 32 general purpose registers, expandable RAM, and a separate memory for the program.



## Importing the program to Factorio

The savefile for the computer is included under the FactorioSave folder, named `Computer.zip`. It can also be imported as a blueprint, see the text file `full_computer.txt` under Blueprints.

## Programming the computer

### By using a symbolic language

This repo comes with its own assembly language. The assembler requires Python 3 and is executed by running `python assembler.py` in a terminal while within the "Assembly" folder. The default file input is `input.fal`, which can be edited with any text editing software. Any syntax errors are shown in terminal output. The output is saved as `output.fal`, and also copied to the clipboard.

See quick_guide.md (TODO: Insert link) for a quick reference on the language.

### By hand

Adventurous people can attempt to program the computer from within Factorio, instruction by instruction. A full overview of the ISA level signal encoding for each instruction can be found here: (!TODO: Insert link). Each 

## Starting the computer

With a new program freshly installed / programmed, you can start the computer by going to the MAN CTR (manual control) module, and turning the constant combinator labelled "START" on or off. The program counter will jump to address 0, and the computer will begin reading the program and executing each instruction.

