# takes in a file and outputs a list of instructions
# an instruction consists of an opcode followed by 0 or more operands

import sys
from instruction import Instruction


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

            operands = " ".join(words[1:])

            instruction = Instruction(opcode, operands, line_n, line)

            instructions.append(instruction)
    
    # replace each branch label with the program address

    unused_labels = set(labels.keys())
    for instruction in instructions:
        e = instruction.operands
        for label in labels:
            if e.find(label) != -1:
                unused_labels.discard(label)
                instruction.operands = e.replace(label, str(labels[label]))

    if len(unused_labels) > 0:
        print("Warning: Unused label(s), {}".format(", ".join(unused_labels)), file=sys.stderr)

    return instructions


# debug
if __name__ == "__main__":
    parse_file("input.fal")
