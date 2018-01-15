# custom exceptions

import sys


class AsmSyntaxError(Exception):
    pass


class ParseOperandError(Exception):
    pass


class ParseFileError(Exception):
    pass


def show_syntax_error(msg, raw_line_str, line_number, index=-1):
    """Show a message to stderr, then exit"""
    # TODO: Accept token as context?
    # TODO: Other types of error? Cyclic dependency for instance isn't syntax error.
    indent_len = 4
    error_msg = "  Line {}\n".format(line_number)
    error_msg += " " * indent_len + raw_line_str + "\n"
    space_offset = 0 if index == -1 else index
    error_msg += " " * (indent_len + space_offset) + "^\n"
    error_msg += "SyntaxError: " + msg
    print(error_msg, file=sys.stderr)
    exit(0)
