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
                    elem.prefix_position += 1
                    result.append(elem)
        return self.closure(result)

    def canonicalCollection(self):
        result = [self.closure([AnalysisElement(Production(self.start_symbol, self.productions_for_a_given_non_terminal(self.start_symbol)[0]), 0)])]
        index = 0
        while index < len(result):
            for elem in result[index]:
                for symbol in elem.production.right_hand_side[elem.prefix_position:]:
                    newState = self.goto(elem, symbol)
                    if len(newState) > 0:
                        result.append(newState)
            index += 1
        return result
