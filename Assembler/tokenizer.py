# Takes in a code file, creates list of filelines where each fileline is a list of tokens

import os
import sys
import time
import label as lb
from enum import Enum, auto
from exceptions import show_syntax_error


class TokenType(Enum):
    UNKNOWN = auto()
    DELIMITER = auto()
    LABEL_SYMBOLIC = auto()
    LABEL_NUMERIC = auto()
    LABEL_DELIMITER = auto()
    OPCODE = auto()
    OPERAND = auto()


class Token:
    def __init__(self, text, t_type, file_line_num, file_raw_text, file_index_start, tokens):
        self.text = text
        self.t_type = t_type
        self.file_line_num = file_line_num
        self.file_raw_text = file_raw_text.strip("\n")
        self.str_col = file_index_start
        self.tokens = tokens
        self.original_token = None  # If copied from a macro, link to original token here

    def copy(self):
        new_token = Token(self.text, self.t_type, self.file_line_num, self.file_raw_text, self.str_col, self.tokens)
        new_token.original_token = self
        return new_token


def tokenize_file(filename):
    tokenized_lines = list()
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line_of_tokens = list()
            delimiters = "[],"

            no_comment = line.split(";", 1)[0]
            if len(no_comment.split()) == 0:
                continue

            found_opcode = False
            start_token = -1  # sentinel value -1: no start token index
            for index, c in enumerate(no_comment):
                if c.isspace() or c in delimiters or c == ":":
                    if start_token != -1:
                        token_txt = no_comment[start_token:index]
                        token_type = TokenType.OPERAND
                        if not found_opcode:
                            token_type = TokenType.OPCODE
                            found_opcode = True
                        token_i = start_token
                        start_token = -1

                        token = Token(token_txt, token_type, i + 1, line, token_i, line_of_tokens)
                        line_of_tokens.append(token)
                    if c in delimiters:
                        token_txt = c
                        token_type = TokenType.DELIMITER
                        token = Token(token_txt, token_type, i + 1, line, index, line_of_tokens)
                        line_of_tokens.append(token)
                    elif c == ":":
                        found_opcode = False
                        if len(line_of_tokens) == 0:
                            # Missing label error
                            error_token = Token(":", TokenType.DELIMITER, i + 1, line, 0, line_of_tokens)
                            show_syntax_error("Missing label", error_token)
                        if line_of_tokens[-1].t_type not in [TokenType.OPCODE, TokenType.LABEL_SYMBOLIC,
                                                             TokenType.LABEL_NUMERIC]:
                            # Invalid label error
                            prev_token = line_of_tokens[-1]
                            show_syntax_error("Invalid label", prev_token)
                        if lb.is_numeric_label(line_of_tokens[-1].text):
                            line_of_tokens[-1].t_type = TokenType.LABEL_NUMERIC
                        else:
                            line_of_tokens[-1].t_type = TokenType.LABEL_SYMBOLIC
                        token_type = TokenType.LABEL_DELIMITER

                        token = Token(c, token_type, i + 1, line, index, line_of_tokens)
                        line_of_tokens.append(token)
                else:
                    # in a token, or beginning a new token
                    if start_token == -1:
                        start_token = index
            tokenized_lines.append(line_of_tokens)

    return tokenized_lines


def _test():
    verbose_out = False

    print("Running test on tokenizer...")

    filename = "abcdefgh_testing_tokenizer.txt"

    test_lines = [
        "#def       end_index 64 ; some comment or some such",
        "lb: STORE $0, [stack_reg]",
        "STORE R0, [R3, mem_start] ; another comment",
        "1: MOV R2, 42"
    ]

    expected_output = [
        ["#def", "end_index", "64"],
        ["lb", ":", "STORE", "$0", ",", "[", "stack_reg", "]"],
        ["STORE", "R0", ",", "[", "R3", ",", "mem_start", "]"],
        ["1", ":", "MOV", "R2", ",", "42"]
    ]

    expected_types = [
        [TokenType.OPCODE, TokenType.OPERAND, TokenType.OPERAND],
        [TokenType.LABEL_SYMBOLIC, TokenType.LABEL_DELIMITER, TokenType.OPCODE, TokenType.OPERAND, TokenType.DELIMITER,
         TokenType.DELIMITER, TokenType.OPERAND, TokenType.DELIMITER],
        [TokenType.OPCODE, TokenType.OPERAND, TokenType.DELIMITER, TokenType.DELIMITER, TokenType.OPERAND,
         TokenType.DELIMITER, TokenType.OPERAND, TokenType.DELIMITER],
        [TokenType.LABEL_NUMERIC, TokenType.LABEL_DELIMITER, TokenType.OPCODE, TokenType.OPERAND, TokenType.DELIMITER,
         TokenType.OPERAND]
    ]

    print("creating testfile:", filename)

    time.sleep(0.005)  # Synchronise stdout, stderr

    with open(filename, "w") as f:
        for line in test_lines:
            f.write(line + "\n")

    # now test the data

    resulting_tokens = tokenize_file(filename)

    # Print out result
    if verbose_out:
        for line in resulting_tokens:
            print([_.file_index_start for _ in line])
            for token in line:
                print(token.text.ljust(10), "=>", str(token.t_type)[10:])
            print("\n")

    test_error_count = 0

    for i, line in enumerate(resulting_tokens):
        for j, token in enumerate(line):
            try:
                assert (token.text == expected_output[i][j])
            except AssertionError:
                test_error_count += 1
                context = "Line index {}, token index {}\n".format(i, j)
                error_msg = "  expected `{}`, but was `{}`".format(expected_output[i][j], token.text)
                print(context, error_msg, sep="", file=sys.stderr)
            try:
                assert (token.t_type == expected_types[i][j])
            except AssertionError:
                test_error_count += 1
                context = "Line index {}, token index {}\n".format(i, j)
                error_msg = "  expected `{}`, but was `{}`".format(expected_types[i][j], token.t_type)
                print(context, error_msg, sep="", file=sys.stderr)

    time.sleep(0.005)

    # delete the file afterwards
    print("deleting testfile:", filename)
    if test_error_count == 0:
        print("All tests succeeded")
    else:
        print("{} test{} failed".format(test_error_count, "" if test_error_count == 1 else "s"))
    os.remove(filename)


if __name__ == "__main__":
    _test()
