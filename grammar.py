import re


class Grammar:
    def __init__(self):
        self.non_terminals = list()
        self.terminals = list()
        self.start_symbol = ""
        self.productions = dict()

    def read_grammar_from_file(self, file_path):
        with open(file_path) as grammar_file:
            self.non_terminals = grammar_file.readline().strip().split(',')

            self.terminals = [terminal.replace(r'\,', ',')
                              for terminal in re.split(r"(?<!\\),",
                                                       grammar_file.readline().strip())]

            self.start_symbol = grammar_file.readline().strip()
            for production in grammar_file.readlines():
                left_hand_side, right_hand_side = production.strip().split('->', maxsplit=1)
                left_hand_side = re.split(r";", left_hand_side)
                if len(left_hand_side) > 1:
                    left_hand_side = tuple(left_hand_side)
                else:
                    left_hand_side = left_hand_side[0]

                self.productions[left_hand_side] = list()
                for current_non_terminal_production in right_hand_side.split("|"):
                    self.productions[left_hand_side].append([current_production.replace(r'\;', ';')
                                                             for current_production in re.split(r"(?<!\\);",current_non_terminal_production)])

    def productions_for_a_given_non_terminal(self, non_terminal):
        return self.productions[non_terminal] if non_terminal in self.non_terminals else "Invalid non-terminal"

    def cfg_check(self):
        for left_hand_side in self.productions.keys():
            if left_hand_side not in self.non_terminals:
                print(left_hand_side)
                return False
        return True
