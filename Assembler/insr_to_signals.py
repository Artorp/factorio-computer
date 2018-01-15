# takes a list of instructions and generates list of signals for the constant combinators PROM

import sys

from instruction import Instruction
from exceptions import ParseOperandError, show_syntax_error
from tokenizer import TokenType
import integer_literal as int_l
import registers
from enum import Enum, auto


class OperandType(Enum):
    REGISTER = auto()
    IMMEDIATE = auto()
    REG_OR_IMM_OR_BOTH = auto()
    REG_OR_IMM = auto()
    REG_OR_LABEL = auto()


opcodes = dict()


def tag(opcode):
    """Add function to opcode map"""
    return lambda func: opcodes.setdefault(opcode.upper(), func)


def inst_to_signals(instructions):
    const_comb_signals = list()

    for inst in instructions:
        assert isinstance(inst, Instruction)
        opcode = inst.opcode_t.text
        if opcode.upper() not in opcodes:
            show_syntax_error("Unknown opcode {}".format(opcode),
                              inst.opcode_t.file_raw_text, inst.opcode_t.file_number, inst.opcode_t.str_col)
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
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}],
        [OperandType.REG_OR_IMM_OR_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("LOAD")
def store_inst(instruction):
    signals = {"copper-plate": 4}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM_OR_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("B")
def b_inst(instruction):
    signals = {"copper-plate": 7}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("BZ")
def bz_inst(instruction):
    signals = {"copper-plate": 7, "signal-C": 1}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("BN")
def bn_inst(instruction):
    signals = {"copper-plate": 7, "signal-C": 2}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("ALU")
def alu_inst(instruction):
    signals = {"copper-plate": 9}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}],
        [OperandType.IMMEDIATE, {"signal-O": "var"}],
        [OperandType.IMMEDIATE, {"signal-2": "var"}],
        [OperandType.IMMEDIATE, {"signal-3": "var"}],
        [OperandType.IMMEDIATE, {"signal-F": "var"}],
        [OperandType.IMMEDIATE, {"signal-red": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("MOV")
def mov_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("ADD")
def add_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("SUB")
def sub_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("INC")
def inc_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1, "signal-B": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var", "signal-K": 1, "signal-0": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("DEC")
def dec_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1, "signal-B": -1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var", "signal-K": 1, "signal-0": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("CMP")
def cmp_inst(instruction):
    signals = {"copper-plate": 9, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("TST")
def add_inst(instruction):
    signals = {"copper-plate": 9, "signal-2": 1}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("MUL")
def mul_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("DIV")
def div_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 2, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("POW")
def pow_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 3, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("MOD")
def mod_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 4, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("ASR")
def asr_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 5, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("LSL")
def lsl_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 6, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("LSR")
def lsr_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 7, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("ROL")
def rol_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 8, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("ROR")
def ror_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 9, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("NOT")
def not_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 10, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("AND")
def and_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 11, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("OR")
def or_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 12, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


@tag("XOR")
def xor_inst(instruction):
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 13, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return iterate_operands(instruction, signals, encoding)


def iterate_operands(inst: Instruction, sig_dict, encoding):
    result_signals = dict()
    result_signals.update(sig_dict)
    operands = extract_operands(inst.operands_t)
    if len(operands) != len(encoding):
        t = inst.opcode_t
        show_syntax_error("Incorrect number of operands, was {} but expected {}".format(len(operands), len(encoding)),
                          t.file_raw_text, t.file_number, t.str_col + len(t.text))
    for i, e in enumerate(operands):
        operand_signals = get_signals_by_operand(e, encoding[i])
        result_signals.update(operand_signals)
    return result_signals


def get_signals_by_operand(operand, operand_type_w_signals):
    operand_dict = dict()
    operand_type = operand_type_w_signals[0]
    signal_dict = operand_type_w_signals[1]
    if operand_type == OperandType.IMMEDIATE:
        val = immediate_from_operand(operand)
        operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type == OperandType.REGISTER:
        val = register_from_operand(operand)
        operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type in [OperandType.REG_OR_IMM, OperandType.REG_OR_LABEL]:
        # label is now a value, so same logic as register / imm
        # Must see if operand has register or value
        last_signal_dict = operand_type_w_signals[2]
        if int_l.is_number_or_literal(operand.text):
            val = immediate_from_operand(operand)
            operand_dict.update(replace_val_in_dict(last_signal_dict, val))
        else:
            val = register_from_operand(operand)
            operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type == OperandType.REG_OR_IMM_OR_BOTH:
        # operand is a list, check length
        last_signal_dict = operand_type_w_signals[2]
        if len(operand) == 2:
            # both reg and imm
            reg = register_from_operand(operand[0])
            imm = immediate_from_operand(operand[1])
            operand_dict.update(replace_val_in_dict(signal_dict, reg))
            operand_dict.update(replace_val_in_dict(last_signal_dict, imm))
        elif len(operand) == 1:
            # must check if operand is register or immediate value
            if int_l.is_number_or_literal(operand[0].text):
                val = immediate_from_operand(operand[0])
                operand_dict.update(replace_val_in_dict(last_signal_dict, val))
            else:
                val = register_from_operand(operand[0])
                operand_dict.update(replace_val_in_dict(signal_dict, val))
        else:
            raise Exception("Unknown error: Extracted bracket operand has no length")
    return operand_dict


def immediate_from_operand(operand):
    val = operand.text
    if not int_l.is_number_or_literal(val):
        show_syntax_error("invalid number {}, must be on format [-][0x|0b]nnnn".format(val),
                          operand.file_raw_text, operand.file_number, operand.str_col)
    num = int_l.to_number_or_literal(val)
    if not int_l.verify_number_range(num):
        show_syntax_error("Immediate number outside signed 32-bit range. Must be within -2^31..2^31 -1. Was: " + num,
                          operand.file_raw_text, operand.file_number, operand.str_col)
    return num


def register_from_operand(operand):
    val = operand.text
    if val.upper() not in registers.register_dict:
        show_syntax_error("Unknown register " + val,
                          operand.file_raw_text, operand.file_number, operand.str_col)
    return registers.register_dict[val.upper()]


def replace_val_in_dict(sym_d, val):
    for key in sym_d:
        if sym_d[key] == "var":
            sym_d[key] = val
    return sym_d


def extract_operands(operand_tokens):
    """
    Takes in a list of tokens, and extracts the operands
    Brackets are grouped as a list.
    """
    result = list()
    active_bracket_group = None
    for t in operand_tokens:
        if t.text == "[":
            if active_bracket_group is not None:
                show_syntax_error("Can't open a bracket within another bracket.",
                                  t.file_raw_text, t.file_number, t.str_col)
            active_bracket_group = list()
        elif t.text == "]":
            if len(active_bracket_group) == 0:
                show_syntax_error("Invalid content in bracket group",
                                  t.file_raw_text, t.file_number, t.str_col)
            result.append(active_bracket_group)
            active_bracket_group = None
        elif t.text == ",":
            continue
        else:
            if active_bracket_group is not None:
                # append to bracket group
                active_bracket_group.append(t)
            else:
                result.append(t)
    if active_bracket_group is not None:
        t = operand_tokens[-1]
        show_syntax_error("Did not close bracket", t.file_raw_text, t.file_number, t.str_col)
    return result
