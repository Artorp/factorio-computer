# Takes in a dictionary of macroes, checks if they have cyclic dependencies

import time
from exceptions import show_syntax_error
from tokenizer import tokenize_file
from token_parser import token_parser


class MacroWrapper:
    def __init__(self, macro):
        self.macro = macro
        self.found = False
        self.finished = False
        self.parent = None
        self.num_active_deps = 0
        self.dependencies = set()


def check_dependencies(macros, verbose=False):
    if len(macros) < 2:
        print("{}, skipping dependency check".format(
            "No macros found" if len(macros) == 0 else "Only one macro found"
        ))
        return
    # Wrap all macros
    wrapped_macros = dict()
    for macro in macros:
        m = macros[macro]
        wrap = MacroWrapper(m)
        wrapped_macros[m.name] = wrap
    # Build dependencies graph
    for w_key in wrapped_macros:
        w = wrapped_macros[w_key]
        for token_line in w.macro.lines_of_inst:
            for token in token_line:
                if token.text == w.macro.name:
                    show_syntax_error("A macro cannot reference itself, infinite recursion",
                                      token.file_raw_text,
                                      token.file_number,
                                      token.str_col)
                if token.text in macros:
                    w.dependencies.add(wrapped_macros[token.text])

    # print dependencies
    if verbose:
        print("Macro dependencies:")
        deps = dict()
        for w_key in wrapped_macros:
            w = wrapped_macros[w_key]
            name = w.macro.name
            names = list()
            for d in w.dependencies:
                names.append(d.macro.name)
            deps[name] = names
        for name in deps:
            print(name + ": " + " ".join(deps[name]))
        time.sleep(0.005)

    # Use DFS on all nodes to detect cyclic dependencies
    for m_key in wrapped_macros:
        m = wrapped_macros[m_key]
        if not m.found:
            # perform iterative DFS
            # https://stackoverflow.com/questions/39074884/edge-classification-in-iterative-dfs
            stack = [m]
            while len(stack) > 0:
                node = stack.pop()
                assert isinstance(node, MacroWrapper)
                if not node.found:
                    if node is not m:
                        # The "root" node isn't considered discovered
                        node.found = True
                    for nabo in node.dependencies:
                        if nabo.found:
                            if not nabo.finished:
                                # Backwards edge, leads to edge found but not finished
                                cycle_reverse = [nabo.macro.name]
                                n = node
                                while n != nabo:
                                    cycle_reverse.append(n.macro.name)
                                    n = n.parent
                                cycle_reverse.append(nabo.macro.name)
                                cycle_readable = " => ".join(reversed(cycle_reverse))
                                t = nabo.macro.begin_token
                                show_syntax_error("Found cyclic dependency in macro. Leads to infinite recursion.\n"
                                                  + " " * 13 + "Cycle: "+cycle_readable,
                                                  t.file_raw_text,
                                                  t.file_number,
                                                  t.str_col)
                            nabo.parent.num_active_deps -= 1
                        node.num_active_deps += 1
                        nabo.parent = node
                        stack.append(nabo)
                    while node is not None and node.num_active_deps == 0:
                        node.finished = True
                        node = node.parent
                        if node is not None:
                            node.num_active_deps -= 1
    if verbose:
        print("No cyclic dependencies found in macros")


if __name__ == "__main__":
    input_filename = "temp_test_cycle.fal"
    tokens_lines_list = tokenize_file(input_filename)
    ms = token_parser(tokens_lines_list)

    check_dependencies(ms)
