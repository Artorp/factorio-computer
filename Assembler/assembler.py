# Assembles a Factorio computer program file into a blueprint

# input: input.fal
# output: output.txt

import os
import platform
import time
import constants
from instruction import Instruction
from file_parser import parse_file
from insr_to_signals import inst_to_signals
from blueprint_generator import Blueprint
from blueprint_import_export import bp_compress, bp_encode_base64
import json


def main():
    file_in = constants.DEFAULT_INPUT_FILE
    file_preprocessed = constants.DEFAULT_PREPROCESSED_FILE
    file_out = constants.DEFAULT_OUTPUT_FILE

    print(file_in)
    time.sleep(0.001)  # If print to stderr, let stdout output first

    instructions = parse_file(file_in)

    with open(file_preprocessed, "w") as f:
        for inst in instructions:
            assert isinstance(inst, Instruction)
            line = inst.opcode.ljust(5) + " "
            line += inst.operands
            f.write(line + "\n")
    
    combinator_signals = inst_to_signals(instructions)

    # print(combinator_signals)

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
