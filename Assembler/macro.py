# macro object class


class Macro:
    def __init__(self, name, param_count, line_begin, begin_token):
        self.name = name
        self.param_count = param_count
        self.token_line_begin = line_begin
        self.token_line_end = -1
        self.begin_token = begin_token
        self.lines_of_inst = list()
