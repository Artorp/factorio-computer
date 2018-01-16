# Takes in the possible opcodes and generates a readable overview of all instructions


from collections import OrderedDict
from opcode_map import opcodes
from operand_type import OperandType as OpTy


def make_opcodes_readable():
    operand_readable = {
        OpTy.REGISTER: "R",
        OpTy.IMMEDIATE: "I",
        OpTy.REG_OR_IMM: "R/I",
        OpTy.REG_OR_IMM_OR_BOTH: "[R/I/R,I]",
        OpTy.REG_OR_LABEL: "R/L"
    }
    encodings = OrderedDict()
    for opcode in opcodes:
        sig, enc = opcodes[opcode]()
        encoding = list()
        for e in enc:
            encoding.append(e[0])
        encodings[opcode] = encoding
    readable_opcodes = ""
    for opcode in encodings:
        readable_opcodes += opcode
        for encoding in encodings[opcode]:
            readable_opcodes += " {},".format(operand_readable[encoding])
        if len(encodings[opcode]) > 0:
            # remove last comma
            readable_opcodes = readable_opcodes[:-1]
        # readable_opcodes += " | action | example"
        readable_opcodes += "\n"
    print(readable_opcodes)


if __name__ == "__main__":
    make_opcodes_readable()
