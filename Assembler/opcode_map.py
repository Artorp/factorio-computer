# all opcodes and their signals are programmed here

from collections import OrderedDict
from operand_type import OperandType
import registers as reg


opcodes = OrderedDict()


def tag(opcode):
    """Add function to opcode map"""
    return lambda func: opcodes.setdefault(opcode.upper(), func)


@tag("HLT")
def hlt_inst():
    return dict(), []


@tag("HLTG")
def hltg_inst():
    signals = {"copper-plate": 6, "signal-cyan": 1, "signal-A": 1}
    return signals, []


@tag("HLTB")
def hltb_inst():
    signals = {"copper-plate": 6, "signal-cyan": 1, "signal-A": 2}
    return signals, []


@tag("NOP")
def nop_inst():
    return {"copper-plate": 1}, []


@tag("STORE")
def store_inst():
    signals = {"copper-plate": 2}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}],
        [OperandType.REG_OR_IMM_OR_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("LOAD")
def store_inst():
    signals = {"copper-plate": 4}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM_OR_BOTH,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("PUSH")
def push_inst():
    signals = {"copper-plate": 13, "signal-K": 1, "signal-0": reg.register_dict["SP"], "signal-A": 0, "signal-O": -1,
               "signal-2": 1, "signal-red": 1, "signal-U": reg.register_dict["SP"]}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("POP")
def pop_inst():
    signals = {"copper-plate": 16, "signal-K": 1, "signal-0": reg.register_dict["SP"], "signal-A": 1,
               "signal-2": 1, "signal-red": 1, "signal-V": reg.register_dict["SP"], }
    encoding = [
        [OperandType.REGISTER,
         {"signal-U": "var"}]
    ]
    return signals, encoding


@tag("B")
def b_inst():
    signals = {"copper-plate": 7}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("BZ")
def bz_inst():
    signals = {"copper-plate": 7, "signal-C": 1}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("BN")
def bn_inst():
    signals = {"copper-plate": 7, "signal-C": 2}
    encoding = [
        [OperandType.REG_OR_LABEL,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("CMEM")
def cmem_inst():
    signals = {"copper-plate": 12, "signal-grey": 1, "signal-black": 1}
    return signals, []


@tag("CREG")
def creg_inst():
    signals = {"copper-plate": 12, "signal-grey": 1}
    return signals, []


@tag("CRAM")
def creg_inst():
    signals = {"copper-plate": 12, "signal-black": 1}
    return signals, []


@tag("ALU")
def alu_inst():
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
    return signals, encoding


@tag("MOV")
def mov_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("ADD")
def add_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("SUB")
def sub_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("INC")
def inc_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1, "signal-B": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var", "signal-K": 1, "signal-0": "var"}]
    ]
    return signals, encoding


@tag("DEC")
def dec_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-2": 1, "signal-3": 1, "signal-B": -1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var", "signal-K": 1, "signal-0": "var"}]
    ]
    return signals, encoding


@tag("CMP")
def cmp_inst():
    signals = {"copper-plate": 9, "signal-2": 1, "signal-3": -1}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("TST")
def add_inst():
    signals = {"copper-plate": 9, "signal-2": 1}
    encoding = [
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}]
    ]
    return signals, encoding


@tag("MUL")
def mul_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 1, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("DIV")
def div_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 2, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("POW")
def pow_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 3, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("MOD")
def mod_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 4, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("ASR")
def asr_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 5, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("LSL")
def lsl_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 6, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("LSR")
def lsr_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 7, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return signals, encoding


@tag("ROL")
def rol_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 8, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return signals, encoding


@tag("ROR")
def ror_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 9, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return signals, encoding


@tag("NOT")
def not_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 10, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
    ]
    return signals, encoding


@tag("AND")
def and_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 11, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("OR")
def or_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 12, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding


@tag("XOR")
def xor_inst():
    signals = {"copper-plate": 9, "signal-red": 1, "signal-F": 13, "signal-2": 1, "signal-3": 1}
    encoding = [
        [OperandType.REGISTER, {"signal-U": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-K": 1, "signal-0": "var"}, {"signal-A": "var"}],
        [OperandType.REG_OR_IMM,
         {"signal-L": 1, "signal-1": "var"}, {"signal-B": "var"}]
    ]
    return signals, encoding
