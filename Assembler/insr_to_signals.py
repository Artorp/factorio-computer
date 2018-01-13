# takes a list of instructions and generates list of signals for the constant combinators PROM

import sys

from instruction import Instruction
from exceptions import ParseOperandError
from operand_parser import OperandType, parse_operand
import registers

opcodes = dict()


def tag(opcode):
    """Add function to opcode map"""
    return lambda func: opcodes.setdefault(opcode.upper(), func)


def inst_to_signals(instructions):
    const_comb_signals = list()

    for inst in instructions:
        assert isinstance(inst, Instruction)
        opcode = inst.opcode
        if opcode.upper() not in opcodes:
            show_syntax_error("unknown opcode {}".format(opcode), inst.raw_instruction, inst.line)
        instruction_signals = opcodes[opcode.upper()](inst)

        const_comb_signals.append(instruction_signals)

    return const_comb_signals


@tag("HLT")
def hlt_inst(instruction):
    return dict()


@tag("NOP")
def nop_inst(instruction):
    return {"copper-plate": 1}


@tag("STORE")
def store_inst(instruction):
    signals = {"copper-plate": 2}
    encoding = [
        [OperandType.REGISTER, {"signal-L": 1, "signal-1": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("LOAD")
def store_inst(instruction):
    signals = {"copper-plate": 4}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("B")
def b_inst(instruction):
    signals = {"copper-plate": 7}
    encoding = [
        [OperandType.REGISTER_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("BZ")
def bz_inst(instruction):
    signals = {"copper-plate": 7, "signal-C": 1}
    encoding = [
        [OperandType.REGISTER_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("BN")
def bn_inst(instruction):
    signals = {"copper-plate": 7, "signal-C": 2}
    encoding = [
        [OperandType.REGISTER_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("ALU")
def alu_inst(instruction):
    signals = {"copper-plate": 9}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}],
        [OperandType.IMMEDIATE, {"signal-O": "var"}],
        [OperandType.IMMEDIATE, {"signal-2": "var"}],
        [OperandType.IMMEDIATE, {"signal-3": "var"}],
        [OperandType.IMMEDIATE, {"signal-F": "var"}],
        [OperandType.IMMEDIATE, {"signal-red": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("MOV")
def mov_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("ADD")
def add_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("SUB")
def sub_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("CMP")
def cmp_inst(instruction):
    signals = {"copper-plate": 9, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("TST")
def add_inst(instruction):
    signals = {"copper-plate": 9, "signal-2": 1}
    encoding = [
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("MUL")
def mul_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("DIV")
def div_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 2, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("POW")
def pow_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 3, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("MOD")
def mod_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 4, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("ASR")
def asr_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 5, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("LSL")
def lsl_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 6, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("LSR")
def lsr_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 7, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("ROL")
def rol_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 8, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("ROR")
def ror_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 9, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("NOT")
def not_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 10, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("AND")
def and_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 11, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("OR")
def or_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 12, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


@tag("XOR")
def xor_inst(instruction):
    signals = {"copper-plate": 9, "signal-F": 13, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.OR_REGISTER_IMMEDIATE,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    iterate_operands(instruction, signals, encoding)
    return signals


def iterate_operands(inst: Instruction, sig_dict, encoding):
    operands = split_instruction(inst.operands)
    if len(operands) != len(encoding):
        show_syntax_error("Incorrect number of opcodes, was {} but expected {}".format(len(operands), len(encoding)),
                          inst.raw_instruction, inst.line)
    for i, e in enumerate(operands):
        add_signals(sig_dict, encoding[i], e, inst.raw_instruction, inst.line)


def add_signals(signals, encoding, operand: str, raw_inst, file_line):
    try:
        if encoding[0] == OperandType.OR_REGISTER_IMMEDIATE_BOTH:
            if not operand.startswith("[") or not operand.endswith("]"):
                show_syntax_error("Register indirect must be wrapped in brackets. E.g.: [R0]",
                                  raw_inst, file_line)
            operand = operand.strip("[]")
            reg, imm, i = parse_operand(operand, 0, encoding[0])
            reg_signals = encoding[1]
            imm_signals = encoding[2]
            if reg is not None:
                for signal_name in reg_signals:
                    if reg_signals[signal_name] == "var":
                        reg_signals[signal_name] = registers.register_dict[reg]
                signals.update(reg_signals)
            if imm is not None:
                for signal_name in imm_signals:
                    if imm_signals[signal_name] == "var":
                        imm_signals[signal_name] = imm
                signals.update(imm_signals)
        elif encoding[0] == OperandType.REGISTER_OR_LABEL or encoding[0] == OperandType.OR_REGISTER_IMMEDIATE:
            val, i = parse_operand(operand, 0, encoding[0])
            reg_signals = encoding[1]
            val_signals = encoding[2]
            if val in registers.register_dict:
                # treat as register
                reg = registers.register_dict[val]
                for signal_name in reg_signals:
                    if reg_signals[signal_name] == "var":
                        reg_signals[signal_name] = reg
                signals.update(reg_signals)
            else:
                for signal_name in val_signals:
                    if val_signals[signal_name] == "var":
                        val_signals[signal_name] = val
                signals.update(val_signals)
        else:
            val, i = parse_operand(operand, 0, encoding[0])
            if val in registers.register_dict:
                val = registers.register_dict[val]
            sigs = encoding[1]
            for signal_name in sigs:
                if sigs[signal_name] == "var":
                    sigs[signal_name] = val
            signals.update(sigs)
    except ParseOperandError as e:
        context = e.args[0]
        index = -1 if "index" not in context else context["index"]
        show_syntax_error(context["msg"], raw_inst, file_line, index)


def split_instruction(instruction):
    splat = [_.strip() for _ in instruction.split(",")]
    if "[" not in instruction and "]" not in instruction:
        return splat
    grouped = []
    join_next = False
    for i, e in enumerate(splat):
        if join_next:
            grouped[-1] += ","+e
        else:
            grouped.append(e)
        join_next = "[" in e
        if join_next and "]" in e:
            join_next = False
    return grouped


def show_syntax_error(msg, raw_line_str, line_number, index=-1):
    error_msg = "  Line {}\n".format(line_number)
    error_msg += "    " + raw_line_str + "\n"
    space_offset = 0 if index == -1 else index - 1
    error_msg += " " * (4 + space_offset) + "^\n"
    error_msg += "SyntaxError: " + msg
    print(error_msg, file=sys.stderr)
    exit(0)
