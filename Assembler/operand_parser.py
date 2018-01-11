from enum import Enum, auto
from registers import register_dict
from integer_literal import is_number_or_literal, to_number_or_literal
from exceptions import ParseOperandError


class OperandType(Enum):
    REGISTER = auto()
    IMMEDIATE = auto()
    OR_REGISTER_IMMEDIATE_BOTH = auto()
    OR_REGISTER_IMMEDIATE = auto()
    REGISTER_OR_LABEL = auto()


def parse_operand(operand, start_index, operand_type):
    if operand_type is OperandType.REGISTER:
        return parse_register(operand, start_index)
    elif operand_type is OperandType.IMMEDIATE:
        return parse_immediate(operand, start_index)
    elif operand_type is OperandType.OR_REGISTER_IMMEDIATE_BOTH:
        return parse_register_or_immediate_or_both(operand, start_index)
    elif operand_type is OperandType.OR_REGISTER_IMMEDIATE:
        return parse_register_or_immediate(operand, start_index)
    elif operand_type is OperandType.REGISTER_OR_LABEL:
        return parse_register_or_label(operand, start_index)


def parse_register(operand, start_index):
    i = skip_whitespace(operand, start_index)
    reg_end = get_word_end(operand, i)
    reg = operand[i:reg_end]
    if reg.upper() not in register_dict:
        raise ParseOperandError({
            "msg": "unknown register " + reg,
            "index": i
        })
    i = reg_end
    i = skip_whitespace(operand, i)
    if i < len(operand):
        if operand[i] == ",":
            i += 1
        else:
            raise ParseOperandError({
                "msg": "invalid symbol found: " + operand[i],
                "index": i
            })
    return reg.upper(), i


# <whitespace>str<whitespace>,
def parse_immediate(operand, start_index):
    i = skip_whitespace(operand, start_index)
    j = get_word_end(operand, i)
    unparsed_n = operand[i:j]
    if not is_number_or_literal(unparsed_n):
        raise ParseOperandError({
            "msg": "invalid number {}, must be on format [-][0x|0b]nnnn".format(unparsed_n),
            "index": i
        })
    n = to_number_or_literal(unparsed_n)
    i = skip_whitespace(operand, j)
    if i < len(operand) and operand[i] == ",":
        i += 1
    return n, i


def parse_register_or_immediate_or_both(operand, start_index):
    reg = None
    imm = None

    i = start_index

    try:
        reg, i = parse_register(operand, i)
    except ParseOperandError as e:
        pass

    try:
        imm, i = parse_immediate(operand, i)
    except ParseOperandError as e:
        pass

    if reg is None and imm is None:
        raise ParseOperandError({
            "msg": "invalid register and/or number",
            "index": i
        })

    return reg, imm, i


def parse_register_or_immediate(operand, start_index):
    reg = None
    imm = None

    i = start_index

    try:
        reg, i = parse_register(operand, i)
    except ParseOperandError as e:
        pass

    try:
        imm, i = parse_immediate(operand, i)
    except ParseOperandError as e:
        pass

    if reg is None and imm is None:
        raise ParseOperandError({
            "msg": "invalid register and/or number",
            "index": i
        })

    val = reg if reg is not None else imm

    return val, i


def parse_register_or_label(operand, start_index):
    "Label is actually a number by this point"
    reg = None
    imm = None

    i = start_index

    try:
        reg, i = parse_register(operand, i)
    except ParseOperandError as e:
        pass

    try:
        imm, i = parse_immediate(operand, i)
    except ParseOperandError as e:
        pass

    if reg is None and imm is None:
        raise ParseOperandError({
            "msg": "invalid branch register or label",
            "index": i
        })

    if reg is not None and imm is not None:
        raise ParseOperandError({
            "msg": "both register and label found, only one is permitted",
            "index": i
        })

    val = reg if reg is not None else imm
    return val, i


def skip_whitespace(string, start_index=0):
    i = start_index
    while i < len(string):
        if not string[i].isspace():
            return i
        i += 1
    return i


def get_word_end(string, start_index=0):
    end_symbols = [","]
    i = start_index
    while i < len(string):
        if string[i].isspace() or string[i] in end_symbols:
            break
        i += 1
    return i

