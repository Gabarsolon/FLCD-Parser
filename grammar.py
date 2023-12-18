import re

from analysis_element import AnalysisElement
from production import Production


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

                if left_hand_side not in self.productions:
                    self.productions[left_hand_side] = list()
                for current_non_terminal_production in right_hand_side.split("|"):
                    self.productions[left_hand_side].append(
                        Production(left_hand_side, [current_production.replace(r'\;', ';') for current_production in
                                                    re.split(r"(?<!\\);", current_non_terminal_production)]))

    def productions_for_a_given_non_terminal(self, non_terminal):
        return self.productions[non_terminal] if non_terminal in self.non_terminals else "Invalid non-terminal"

    def cfg_check(self):
        for left_hand_side in self.productions.keys():
            if left_hand_side not in self.non_terminals:
                print(left_hand_side)
                return False
        return True

    def closure(self, analysisElements):
        """

        :param analysisElements: list of AnalysisElement
        :return:
        """
        closure_set = analysisElements
        C_has_been_modified = True
        while C_has_been_modified:
            C_has_been_modified = False
            for analysis_element in closure_set:
                if analysis_element.prefix_position >= len(analysis_element.production.right_hand_side):
                    continue
                B = analysis_element.production.right_hand_side[analysis_element.prefix_position]
                if B not in self.non_terminals:
                    continue
                for b_production in self.productions_for_a_given_non_terminal(B):
                    new_analysis_element = AnalysisElement(b_production, 0)
                    if new_analysis_element not in closure_set:
                        C_has_been_modified = True
                        closure_set.append(new_analysis_element)
        return closure_set

    def goto(self, analysisElements, symbol):
        """

        :param analysisElements:
        :param symbol:
        :return:
        """
        result = list()
        for elem in analysisElements:
            if symbol in elem.production.right_hand_side:
                if elem.production.right_hand_side.index(symbol) == elem.prefix_position:
                    analysis_element_with_shifted_dot = AnalysisElement(elem.production, elem.prefix_position +1)
                    result.append(analysis_element_with_shifted_dot)
        return self.closure(result)

    def canonicalCollection(self):
        result = [self.closure([AnalysisElement(self.productions_for_a_given_non_terminal(self.start_symbol)[0], 0)])]
        # print(result)
        index = 0
        while index < len(result):
            for elem in result[index]:
                for symbol in elem.production.right_hand_side[elem.prefix_position:]:
                    newState = self.goto(result[index], symbol)
                    if len(newState) > 0 and newState not in result:
                        result.append(newState)
            index += 1
        return result

    def get_production_number(self, production):
        #                                                                             ignore S'
        return [production for productions_for_terminal in list(self.productions.values())[1:] for production in productions_for_terminal].index(production)

    def parsing_table(self):
        """
        The table will be represented as a list (as shown bellow)
        State 0 is in the position 0 of the list
        [
            {
                ACTION: ["shift" | "accept" | "r1" | "error,]
                GOTO: {
                    a: 2,
                    A: 3
                    ...
                }
            }
        ]
        :return:
        """
        states = self.canonicalCollection()
        table = []

        for state_index in range(0, len(states)):
            state = states[state_index]
            table_entry = {
                "ACTION": [],
                "GOTO": {}
            }
            for analysis_element in state:
                if analysis_element.prefix_position < len(analysis_element.production.right_hand_side):
                    if "shift" not in table_entry["ACTION"]:
                        table_entry["ACTION"].append("shift")
                    #check which state threats this shift
                    symbol_to_add = analysis_element.production.right_hand_side[analysis_element.prefix_position]
                    for state_to_check_index in range(state_index + 1, len(states)):
                        state_to_check = states[state_to_check_index]

                        first_analysis_element = state_to_check[0]
                        if first_analysis_element.prefix_position > 0:
                            if state_to_check_index == 3:
                                print(first_analysis_element)
                            if first_analysis_element.production.right_hand_side[first_analysis_element.prefix_position - 1] == symbol_to_add:
                                table_entry["GOTO"][symbol_to_add] = state_to_check_index
                                break
                elif analysis_element.prefix_position == len(analysis_element.production.right_hand_side):
                    print(analysis_element)
                    analysis_element_to_check = AnalysisElement(self.productions[self.start_symbol], 1)
                    if analysis_element == AnalysisElement(self.productions[self.start_symbol][0], 1):
                        table_entry["ACTION"].append("accept")
                    else:
                        table_entry["ACTION"].append("r" + str(self.get_production_number(analysis_element.production)))
                else:
                    table_entry["ACTION"].append("error")
            table.append(table_entry)
        return table

    def parse_sequence(self, sequence):
        working_stack = [0]
        input_stack = [sequence.split("")]
        output_band = []

