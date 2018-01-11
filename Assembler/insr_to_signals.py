# takes a list of instructions and generates list of signals for the constant combinators PROM

from instruction import Instruction
import constants
import json
import registers


def inst_to_signals(instructions):
    # TODO: use functions instead of json file
    with open(constants.OPCODE_SIGNALS) as f:
        opcodes_dict = json.load(f)

    const_comb_signals = list()

    for inst in instructions:
        assert isinstance(inst, Instruction)
        opcode = inst.opcode
        if opcode not in opcodes_dict:
            raise Exception("Syntax error, unknown opcode {}".format(opcode))
        inst_dict = opcodes_dict[opcode]
        instruction_signals = dict()
        if "control" in inst_dict:
            instruction_signals = {**instruction_signals, **inst_dict["control"]}
        if "format" in inst_dict:
            for i, f in enumerate(inst_dict["format"]):
                operand = inst[1 + i]
                if f.startswith("reg"):
                    key = f.split("_")[-1]
                    reg_index = register_to_address(operand)
                    add_signals(instruction_signals, inst_dict[key], reg_index)
                elif f.startswith("imm_or_reg"):
                    # two entries this time
                    key = f.split("_")[-1]
                    if "," in operand:
                        _ = operand.strip("[]")
                        reg_str, imm = _.split(",")
                        reg_str = reg_str.strip()
                        imm = imm.strip()
                        reg_i = register_to_address(reg_str)
                        imm = to_number_or_literal(imm)
                        add_signals(instruction_signals, inst_dict["imm_or_reg_" + key + "_reg"], reg_i)
                        add_signals(instruction_signals, inst_dict["imm_or_reg_" + key + "_imm"], imm)
                    else:
                        _ = operand.strip("[]").strip()
                        if is_number_or_literal(_):
                            imm = to_number_or_literal(_)
                            add_signals(instruction_signals, inst_dict["imm_or_reg_" + key + "_imm"], imm)
                        else:
                            reg_i = register_to_address(_)
                            add_signals(instruction_signals, inst_dict["imm_or_reg_" + key + "_reg"], reg_i)
                elif f.startswith("label_reg"):
                    # also two entries
                    key = f.split("_")[-1].strip()
                    if is_number_or_literal(operand):
                        adr = to_number_or_literal(operand)
                        add_signals(instruction_signals, inst_dict["label_" + key + "_lab"], adr)
                    else:
                        reg_i = register_to_address(operand)
                        add_signals(instruction_signals, inst_dict["label_" + key + "_reg"], reg_i)
                elif f.startswith("val"):
                    key = f.split("_")[-1].strip()
                    if not is_number_or_literal(operand):
                        raise Exception("Immediate value must be number or literal, was {}".format(operand))
                    imm = to_number_or_literal(operand)
                    add_signals(instruction_signals, inst_dict["val_" + key], imm)
        const_comb_signals.append(instruction_signals)
    return const_comb_signals


def register_to_address(reg_string):
    if reg_string not in registers.register_dict:
        raise Exception("Unknown register: {}".format(reg_string))
    return registers.register_dict[reg_string]


def add_signals(add_to, add_from, variable):
    for sig in add_from:
        if add_from[sig] == "var":
            add_to[sig] = variable
        else:
            add_to[sig] = add_from[sig]


def is_number_or_literal(n):
    prefix = str(n).lower()
    if prefix.startswith("0x") or prefix.startswith("-0x"):
        try:
            int(n, base=16)
            return True
        except ValueError:
            return False
    elif prefix.startswith("0b") or prefix.startswith("-0b"):
        try:
            int(n, base=2)
            return True
        except ValueError:
            return False
    else:
        try:
            int(n)
            return True
        except ValueError:
            return False


def to_number_or_literal(n):
    prefix = str(n).lower()
    if prefix.startswith("0x") or prefix.startswith("-0x"):
        return int(n, base=16)
    elif prefix.startswith("0b") or prefix.startswith("-0b"):
        return int(n, base=2)
    else:
        return int(n)


# test
if __name__ == "__main__":
    instructions = [['MOV', 'R0', '1'],
                    ['CMP', 'R0', "R2"],
                    ['MOV', 'R1', '0'],
                    ['HLT'],
                    ['ADD', 'R2', 'R0', 'R1'],
                    ['ADD', 'R1', 'R2', "-0x1"],
                    ['LOAD', 'R2', '[R3, 5]'],
                    ["B", 0],
                    ["B", "R4"],
                    ["BN", "R4"],
                    ["ALU", "R2", "R0", "R1", "1", "0x1", "0b1", "0", 0]
                    ]

    signals = inst_to_signals(instructions)

    print(signals)

