# Assembles a Factorio computer program file into a blueprint

# input: input.fal
# output: output.txt

import sys
import os
import time
import constants
from file_parser import parse_file
from insr_to_signals import inst_to_signals
from blueprint_generator import Blueprint
from blueprint_import_export import bp_compress, bp_encode_base64
import json


def main():
    file_in = constants.DEFAULT_INPUT_FILE
    file_out = constants.DEFAULT_OUTPUT_FILE

    print(file_in)
    time.sleep(0.001)  # If print to stderr, let stdout output first

    instructions = parse_file(file_in)
    
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

    # paste to clipboard
    # TODO: Detect OS type, currently only on Windows
    os.system("echo " + output + " | clip")

    print("Done. Blueprint string on clipboard.")


if __name__ == "__main__":
    main()

