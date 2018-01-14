# Takes in a list of list of tokens, and pre-processes them into a list of instructions

from tokenizer import Token
from macro import Macro
from macro_dependencies_checker import check_dependencies
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

    # check for macro dependencies
    check_dependencies(macros)

    # replace all macros with the macro contents
    # remove all macro definitions from tokens
    # traverse macros in reverse order of declaration, to preserve indexes
    for m_key in sorted(macros, key=lambda x: macros[x].token_line_begin, reverse=True):
        m = macros[m_key]
        assert isinstance(m, Macro)
        # token_line_begin and token_line_end
        tokens = tokens[:m.token_line_begin] + tokens[m.token_line_end:]
        print(str(m.begin_token.file_number))

    for m_key in macros:
        m = macros[m_key]
        print(m_key)
        for line in m.lines_of_inst:
            print([_.text for _ in line])

    print("\n\nBefore replacements\n\n")

    replacement_happened = True
    while replacement_happened:
        replacement_happened = False
        # Traverse the tokens in reverse order, while keeping own index
        index = len(tokens) - 1
        while index >= 0:
            line = tokens[index]
            if line[0].text in macros.keys():
                m = macros[line[0].text]
                if len(line) != 1 + m.param_count:
                    show_syntax_error("Invalid number of macro parameters. Macro expects {}, got {}"
                                      .format(m.param_count, len(line) - 1),
                                      line[0].file_raw_text,
                                      line[0].file_number,
                                      line[0].str_col
                                      )
                params = line[1:]
                # Replace line with body of macro
                line_replace = list()
                for lines in m.lines_of_inst:
                    line = list()
                    for token in lines:
                        new_token = token.copy()
                        line.append(new_token)
                        if new_token.text.startswith("$"):
                            try:
                                num = int(new_token.text[1:])
                                if num > len(params) - 1 or num < 0:
                                    raise ValueError
                                new_token.text = params[num].text
                            except ValueError:
                                show_syntax_error("Parameter must have valid argument index",
                                                  token.file_raw_text, token.file_number, token.str_col)
                    line_replace.append(line)
                tokens = tokens[:index] + line_replace + tokens[index + 1:]
                replacement_happened = True
            index -= 1

    # print("\n\nAfterwards")
    # for line in tokens:
    #     for t in line:
    #         print(t.text + " ", end="")
    #     print()

    # Handle definitions
    # TODO

    return None


def tokens_have_macros(tokens, macros):
    for line in tokens:
        if line[0] in macros:
            return True
