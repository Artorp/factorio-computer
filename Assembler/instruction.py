# This class represents a single line of code


class Instruction():
    def __init__(self, opcode_t, operands_t, line, raw_instruction):
        self.opcode = "UNDEFINED"
        self.opcode_t = opcode_t
        self.operands = "UNDEFINED_OP"
        self.operands_t = operands_t
        self.line = line
        self.raw_instruction = raw_instruction

    def update_texts(self):
        # TODO: This is a temporary function while transitioning to tokens from text
        self.opcode = self.opcode_t.text
        self.operands = " ".join([str(_.text) for _ in self.operands_t])
