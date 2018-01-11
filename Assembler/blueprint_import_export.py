# Imports and exports to the blueprint format used by Factorio
# https://wiki.factorio.com/Blueprint_string_format

import sys
import base64
import zlib

SUPP_BP_VERSION = "0"


def bp_decode_base64(blueprint: str) -> bytes:
    global SUPP_BP_VERSION
    blueprint_version = blueprint[0]
    if blueprint_version is not SUPP_BP_VERSION:
        warning_msg = "Warning: Expected Factorio blueprint version {}, was version {}\n"
        print(warning_msg.format(SUPP_BP_VERSION, blueprint_version), file=sys.stderr)

    blueprint = blueprint[1:]
    return base64.b64decode(blueprint.encode("utf-8"))


def bp_encode_base64(bp_compressed: bytes) -> str:
    global SUPP_BP_VERSION
    return SUPP_BP_VERSION + base64.b64encode(bp_compressed).decode("utf-8")


def bp_decompress(bp_compressed: bytes) -> str:
    return zlib.decompress(bp_compressed).decode("utf-8")


def bp_compress(bp_json: str) -> bytes:
    return zlib.compress(bp_json.encode("utf-8"))



# Notes. TODO: DELETE!

# Assembly order of operations

# 1. take input file
# 2. parse line by line, ignore after ";" as it's comment, save constants (#def x 10) in  first pass, discard #def lines
# 3. 2nd pass, replace each constant from #def hashmap / dict
# 4. 3rd pass, assign each line an index, create dict for labels. When found label, apply to next instruction.
#    if no more instruction found, create NOP instr at end and point to this instruction
# This is valid:
# label: MOV 1 2
# B label
# So is this:
# label:
# MOV 1, 2
# B label
# And this:
# MOV 1, 2
# B label
# label:
# (will jump to end of program, then HALT)
# 5. Begin parsing each instruction. Each instruction is in object with fields / vars:
#    linenr. (for debugging), index, instruction_txt, opcode: str, signals[]
#    Based on OPCODE, calculate applicable signals. something like get_signals(opcode, operands)
#    A signal has a type (item / virtual) and a name (copper-plate / signal-A), and a count (signed 32-bit int)
# 6. Begin creating blueprint JSON. Setup stone walls, for each instruction set Y-coordinate to index,
#    and populate signals. Connect connections where applicable.
#    Keep track of connection. must keep track of previous artihmic-signal, light, and decider output.
# 7. Compress json with zlip
# 8. Encode as base64
# 9. Output to file, and / or put into clipboard
