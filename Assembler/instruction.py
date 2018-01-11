# This class represents a single line of code


class Instruction():
    def __init__(self, opcode, operands, line):
        self.opcode = opcode
        self.operands = operands
        self.line = line

