# The different operand types

from enum import Enum, auto


class OperandType(Enum):
    REGISTER = auto()
    IMMEDIATE = auto()
    REG_OR_IMM_OR_BOTH = auto()
    REG_OR_IMM = auto()
    REG_OR_LABEL = auto()
