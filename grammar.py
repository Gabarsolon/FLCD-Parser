class Grammar:
    def __init__(self):
        self.non_terminals = list()
        self.terminals = list()
        self.start_symbol = ""
        self.productions = dict()

    def read_grammar_from_file(self, file_path):
        with open(file_path) as grammar_file:
            self.non_terminals = grammar_file.readline().strip().split(',')
            self.terminals = grammar_file.readline().strip().split(',')
            self.start_symbol = grammar_file.readline().strip()
            for production in grammar_file.readlines():
                left_hand_side, right_hand_side = production.strip().split('->', maxsplit=1)
                self.productions[left_hand_side] = right_hand_side.split("|")

    def productions_for_a_given_non_terminal(self, non_terminal):
        # TODO
        return None

    def cfg_check(self):
        for left_hand_side in self.productions.keys():
            if left_hand_side not in self.non_terminals:
                return False
        return True
