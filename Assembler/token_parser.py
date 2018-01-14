# Takes in a list of list of tokens, and pre-processes them into a list of instructions

from tokenizer import Token
from macro import Macro
from exceptions import show_syntax_error


def token_parser(tokens):
    # 1st pass, build a table of macros
    macros = dict()
    active_macro = None
    for i, line in enumerate(tokens):
        first_token = line[0]
        assert isinstance(first_token, Token)
        if first_token.text.lower() == "#macro":
            # start new macro
            if active_macro is not None:
                show_syntax_error("Can't define new macro within another macro",
                                  first_token.file_raw_text,
                                  first_token.file_number,
                                  first_token.str_col)

            if len(line) != 3:
                show_syntax_error("Macro start tag needs a declaration, name and number of parameters.\n"
                                  "Example: `#macro name 2`",
                                  first_token.file_raw_text,
                                  first_token.file_number,
                                  first_token.str_col)
            macro_name = line[1].text
            if macro_name in macros:
                show_syntax_error("Macro name must be unique",
                                  line[1].file_raw_text,
                                  line[1].file_number,
                                  line[1].str_col)
            macro_params = -1
            try:
                macro_params = int(line[2].text)
                if macro_params < 0:
                    raise ValueError("")
            except ValueError as ve:
                show_syntax_error("Parameter count must be a non-negative integer",
                                  line[2].file_raw_text,
                                  line[2].file_number,
                                  line[2].str_col)

            active_macro = Macro(macro_name, macro_params, i, first_token)
        elif first_token.text.lower() == "#endm":
            # finish macro definition
            if active_macro is None:
                show_syntax_error("Invalid macro end, no matching macro declaration",
                                  first_token.file_raw_text,
                                  first_token.file_number,
                                  first_token.str_col)
            # Note, index given to macro is the exclusive upper index, so increase index by one
            active_macro.token_line_end = i + 1
            macros[active_macro.name] = active_macro
            active_macro = None
        else:
            if active_macro is not None:
                # Insert instructions as tokens into active macro
                active_macro.lines_of_inst.append(line)
                # TODO: Ensure the copied tokens references the macro
    if active_macro is not None:
        show_syntax_error("Missing `#endm` declaration for declared macro",
                          active_macro.begin_token.file_raw_text,
                          active_macro.begin_token.file_number,
                          active_macro.begin_token.str_col)

    # 2nd pass, build macro dependencies
    return macros
