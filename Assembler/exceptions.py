# custom exceptions


class AsmSyntaxError(Exception):
    pass


class ParseOperandError(Exception):
    pass


class ParseFileError(Exception):
    pass


def show_syntax_error(msg, raw_line_str, line_number, index=-1):
    """Show a message to stderr, then exit"""
    error_msg = "  Line {}\n".format(line_number)
    error_msg += "    " + raw_line_str + "\n"
    space_offset = 0 if index == -1 else index - 1
    error_msg += " " * (4 + space_offset) + "^\n"
    error_msg += "SyntaxError: " + msg
    print(error_msg, file=sys.stderr)
    exit(0)
