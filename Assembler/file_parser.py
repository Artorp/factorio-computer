# takes in a file and outputs a list of instructions
# an instruction consists of an opcode followed by 0 or more operands

import sys
import re
from instruction import Instruction
from exceptions import AsmSyntaxError, ParseFileError, show_syntax_error
import label as l


def parse_file(program_filename):
    instructions = list()
    
    definitions = dict()
    symbolic_labels = dict()
    numeric_labels = list()  # sorted by PC address

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
                target_label = len(instructions)  # value is PC address
                if l.is_numeric_label(label):
                    label_num = l.NumericLabel(int(label), target_label)
                    numeric_labels.append(label_num)
                else:
                    if label in symbolic_labels:
                        error_msg = "Label ´{}´ previously defined".format(label)
                        # TODO: Show which file line the label was defined in
                        show_syntax_error(error_msg, line, line_n)
                    symbolic_labels[label] = target_label
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

    unused_labels = set(symbolic_labels.keys())
    for i, instruction in enumerate(instructions):
        e = instruction.operands
        for label in symbolic_labels:
            if e.find(label) != -1:
                unused_labels.discard(label)
                instruction.operands = e.replace(label, str(symbolic_labels[label]))
        # TODO: Tokenize the input, makes this easier
        # [R5,1b] => 1b
        "".split()
        tokens = re.split("([\s\\[\\],])", instruction.operands)  # Split by: whitespace [ ] ,
        did_replace = False
        for j, token in enumerate(tokens):
            if len(token) == 2 and token[0].isdecimal() and token[1] in ["b", "f"]:
                target_label = None
                try:
                    if token[1] == "b":
                        target_label = l.find_back_label(numeric_labels, int(token[0]), i)
                    elif token[1] == "f":
                        target_label = l.find_forward_label(numeric_labels, int(token[0]), i)
                except AsmSyntaxError as e:
                    show_syntax_error(e.args[0], instruction.raw_instruction, instruction.line)
                tokens[j] = str(target_label.pc_adr)
                target_label.was_referenced = True
                did_replace = True

        if did_replace:
            instruction.operands = "".join(tokens)

    for numeric_label in numeric_labels:
        if not numeric_label.was_referenced:
            unused_labels.add(str(numeric_label.digit))

    if len(unused_labels) > 0:
        print("Warning: Unused label(s), {}".format(", ".join(unused_labels)), file=sys.stderr)

    return instructions


# debug
if __name__ == "__main__":
    parse_file("input.fal")
