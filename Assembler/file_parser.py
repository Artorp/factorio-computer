# takes in a file and outputs a list of instructions
# an instruction consists of an opcode followed by 0 or more operands

import sys
import constants
import json
from instruction import Instruction
from exceptions import AsmSyntaxError


def parse_file(program_filename):
    instructions = list()
    
    definitions = dict()
    labels = dict()

    with open(program_filename) as f:
        for line_n, line in enumerate(f, 1):
            # strip comments
            line = line.split(";")[0]
            line = line.strip()
            
            if line == "":
                continue

            words = line.split()

            # apply definitions
            for i in range(len(words)):
                for key in definitions:
                    words[i] = words[i].replace(key, definitions[key])

            # check for new definitions
            if words[0].upper() == "#DEF":
                k = words[1]
                v = words[2]
                definitions[k] = v
                continue
            
            # check for label
            label_index = words[0].find(":")
            if label_index != -1:
                label = words[0][:label_index]
                labels[label] = len(instructions)  # value is PC address
                remainder = words[0][label_index+1:]
                if remainder == "":
                    words.pop(0)
                else:
                    words[0] = remainder
            
            if len(words) == 0:
                continue
            
            # parse operands


            opcode = words[0]

            operands = " ".join(words[1:]).split(",")  # all operands are comma separated
            if len(operands) == 1 and operands[0] == "":
                operands.pop()

            instruction = Instruction(opcode, operands, line_n)

            instructions.append(instruction)

            # TODO: Remove commented code

            """

            # TODO: create instruction object

            instruction = list()
            instruction.append(words[0].upper())
            
            operands = " ".join(words[1:])
            
            # print("OPCODE:", instruction[0])
            # print("operands:", operands)
            
            instruction += parse_operand_string(operands)
            
            # print("full instruction list:",instruction)
            instructions.append(instruction)
            """
    
    # replace each branch label with the program address

    unused_labels = set(labels.keys())
    for instruction in instructions:
        for i, e in enumerate(instruction.operands):
            if e in labels:
                unused_labels.remove(e)
                instruction.operands[i] = labels[e]

    if len(unused_labels) > 0:
        print("Warning: Unused label(s), {}".format(", ".join(unused_labels)), file=sys.stderr)
    
    return instructions
    

# TODO: Move logic from this func into opcode parser?

def parse_operand_string(op_string):
    operands = []
    begin_op = 0
    i = 0
    while i < len(op_string):
        c = op_string[i]
        if c == "[":
            next_bracket = op_string.find("[", i + 1)
            end_bracket = op_string.find("]", i)
            if next_bracket != -1 and next_bracket < end_bracket:
                raise Exception("Found nested brackets")  # TODO, exit program with error msg
            if end_bracket == -1:
                raise Exception("Brackets not closed")
            op = op_string[i:end_bracket + 1].strip()
            operands.append(op)
            i = end_bracket + 1
            begin_op = i
            continue
        elif c == ",":
            op = op_string[begin_op:i].strip()
            begin_op = i + 1
            if op == "":
                raise Exception("Empty operand at line, col")
            operands.append(op)
        i += 1
    if begin_op < i:
        op = op_string[begin_op:i].strip()
        if op == "":
            raise Exception("Empty operand at line, col")
        operands.append(op)
    
    return operands



# MOV R2, (R2, 4)


# debug
if __name__ == "__main__":
    parse_file("input.fal")

