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


def full_signal_encoding_markdown_table():
    encodings = OrderedDict()
    markdown_table = ""
    for opcode in opcodes:
        markdown_table += "\n### {}\n\nOperand | Signals\n--- | ---\n".format(opcode)
        sig, enc = opcodes[opcode]()
        markdown_table += "Control | "
        for sig_key in sig:
            s = strip_signal(sig_key)
            markdown_table += "{}: {}, ".format(s, sig[sig_key])
        if len(sig) > 0:
            markdown_table = markdown_table[:-2]
        markdown_table += "\n"
        # iterate over each operand
        for i, o in enumerate(enc):
            markdown_table += "Operand_{} | ".format(str(i + 1))
            # TODO: Add each signal, insert <br> if both reg and imm possible
    print(markdown_table)


def strip_signal(signal: str) -> str:
    if signal.startswith("signal-"):
        signal = signal[7:]
    return signal


if __name__ == "__main__":
    full_signal_encoding_markdown_table()
