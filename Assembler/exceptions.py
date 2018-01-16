# custom exceptions

import sys
import time


class AsmSyntaxError(Exception):
    pass


class ParseOperandError(Exception):
    pass


class ParseFileError(Exception):
    pass


def show_parsing_error(msg, token):
    output_error("ParsingError", msg, token)


def show_syntax_error(msg, token):
    output_error("SyntaxError", msg, token)


def output_error(error_type, msg, token):
    """Show a message to stderr, then exit"""
    if "\n" in msg:
        splat = msg.split("\n")
        indented = splat[1:]
        msg = splat[0] + "".join(["\n" + " " * (len(error_type) + 2) + _ for _ in indented])
    error_msg = get_line_from_token(token)
    error_msg += error_type + ": " + msg
    time.sleep(0.005)
    print(error_msg, file=sys.stderr)
    exit(0)


def show_warning(msg, token):
    warning = get_line_from_token(token)
    warning += "Warning: " + msg
    time.sleep(0.005)
    print(warning, file=sys.stderr)


def show_warning_one_line(msg, token):
    warning = "[Warning, line {}] ".format(str(token.file_line_num)) + msg
    time.sleep(0.005)
    print(warning, file=sys.stderr)


def get_line_from_token(token):
    line_number = token.file_line_num
    raw_line = token.file_raw_text
    index = token.str_col
    indent_len = 4
    error_msg = "  Line {}\n".format(line_number)
    error_msg += " " * indent_len + raw_line + "\n"
    error_msg += " " * (indent_len + index) + "^\n"
    return error_msg
