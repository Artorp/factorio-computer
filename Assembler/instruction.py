# This class represents a single line of code


class Instruction:
    # TODO: Drop line number and raw instructions, are in token object
    def __init__(self, opcode, operands, line, raw_instruction):
        self.opcode = opcode
        self.operands = operands
        self.line = line
        self.raw_instruction = raw_instruction
