# Assembles a Factorio computer program file into a blueprint

# input: input.fal
# output: output.txt

import json
import os
import platform
import time

import constants
from blueprint_generator import Blueprint
from blueprint_import_export import bp_compress, bp_encode_base64
from insr_to_signals import inst_to_signals
from instruction import Instruction
from token_parser import token_parser
from tokenizer import tokenize_file


def main():
    file_in = constants.DEFAULT_INPUT_FILE
    file_preprocessed = constants.DEFAULT_PREPROCESSED_FILE
    file_out = constants.DEFAULT_OUTPUT_FILE

    print(file_in)
    time.sleep(0.005)  # If print to stderr, let stdout output first

    lines_of_tokens = tokenize_file(file_in)

    instructions = token_parser(lines_of_tokens)

    with open(file_preprocessed, "w") as f:
        for inst in instructions:
            assert isinstance(inst, Instruction)
            line = inst.opcode.text.ljust(5) + " "
            line += " ".join([str(_.text) for _ in inst.operands])
            f.write(line + "\n")
    
    combinator_signals = inst_to_signals(instructions)

    # create blueprint

    bp = Blueprint()
    bp.generate_rom_entities(len(combinator_signals))
    bp.insert_signals(combinator_signals)

    # export
    json_string = json.dumps(bp.json_dict)
    output = bp_encode_base64(bp_compress(json_string))

    with open(file_out, "w") as f:
        f.write(output+"\n")

    # paste to clipboard, clip on Windows
    if platform.system() == "Windows":
        os.system("clip < " + file_out)
        print("Done. Blueprint string on clipboard.")
    else:
        print("Done. Blueprint string saved as " + file_out)


if __name__ == "__main__":
    main()
