import unittest

from analysis_element import AnalysisElement
from grammar import Grammar
from production import Production
from ParserOutput import ParserOutput


class TestLR0(unittest.TestCase):
    def setUp(self) -> None:
        self.longMessage = True
        self.grammar = Grammar()
        self.parser_output = ParserOutput(self.grammar)
        self.grammar.read_grammar_from_file("input/G1.txt")

    def tearDown(self) -> None:
        pass

    def test_closure(self):
        assert (self.grammar.closure([AnalysisElement(Production("S", ["a", "A"]), 1)])) == [
            AnalysisElement(Production("S", ["a", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]), 0)]

    def test_goto(self):
        analysis_element_set_to_test = [
            AnalysisElement(Production("S", ["a", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]), 0)
        ]

        assert (self.grammar.goto(analysis_element_set_to_test, "b") == [
            AnalysisElement(Production("A", ["b", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]), 0)
        ])

    def test_col_can(self):
        # print(self.grammar.canonicalCollection())
        assert (self.grammar.canonicalCollection() == [
            # s0
            [
                AnalysisElement(Production("S'", ["S"]), 0),
                AnalysisElement(Production("S", ["a", "A"]), 0)
            ],
            # s1
            [
                AnalysisElement(Production("S'", ["S"]), 1)
            ],
            # s2
            [
                AnalysisElement(Production("S", ["a", "A"]), 1),
                AnalysisElement(Production("A", ["b", "A"]), 0),
                AnalysisElement(Production("A", ["c"]), 0)
            ],
            # s3
            [
                AnalysisElement(Production("S", ["a", "A"]), 2)
            ],
            # s4
            [
                AnalysisElement(Production("A", ["b", "A"]), 1),
                AnalysisElement(Production("A", ["b", "A"]), 0),
                AnalysisElement(Production("A", ["c"]), 0)
            ],
            # s5
            [
                AnalysisElement(Production("A", ["c"]), 1),
            ],
            # s6
            [
                AnalysisElement(Production("A", ["b", "A"]), 2)
            ]
        ])

    def test_parsing_table(self):
        assert (self.grammar.parsing_table() ==
                [
                    # s0
                    {
                        'ACTION': ['shift'],
                        'GOTO':
                            {'S': 1, 'a': 2}
                    },
                    # s1
                    {
                        'ACTION': ['accept'],
                        'GOTO': {}
                    },
                    # s2
                    {
                        'ACTION': ['shift'],
                        'GOTO': {'A': 3, 'b': 4, 'c': 5}
                    },
                    # s3
                    {
                        'ACTION': ['r0'],
                        'GOTO': {}
                    },
                    # s4
                    {
                        'ACTION': ['shift'],
                        'GOTO': {'A': 6, 'b': 4, 'c': 5}
                    },
                    # s5
                    {
                        'ACTION': ['r2'],
                        'GOTO': {}
                    },
                    # s6
                    {
                        'ACTION': ['r1'],
                        'GOTO': {}
                    }
                ]
                );

    def test_parse_sequence(self):
        assert (self.grammar.parse_sequence("input/seq.txt") == [0, 1, 1, 2])

    def test_parser_output(self):
        self.parser_output.generateOutputTree(self.grammar.parse_sequence("input/seq.txt"))
        assert (self.parser_output.TreeToList(self.parser_output.root) ==
                [
                    [{'index': 1, 'info': 'S', 'parent': None, 'right_sibling': None}],
                    [{'index': 2, 'info': 'a', 'parent': 'S', 'right_sibling': 'A'}, {'index': 3, 'info': 'A',
                                                                                      'parent': 'S',
                                                                                      'right_sibling': None}],
                    [{'index': 4, 'info': 'b', 'parent': 'A', 'right_sibling': 'A'}, {'index': 5, 'info': 'A',
                                                                                      'parent': 'A',
                                                                                      'right_sibling': None}],
                    [{'index': 6, 'info': 'b', 'parent': 'A', 'right_sibling': 'A'}, {'index': 7, 'info': 'A',
                                                                                      'parent': 'A',
                                                                                      'right_sibling': None}],
                    [{'index': 8, 'info': 'c', 'parent': 'A', 'right_sibling': None}]

                ]
            );

    def test_table_conflicts(self):
        not_lr0_grammar = Grammar()
        not_lr0_grammar.read_grammar_from_file("input/G1_not_lr0.txt")
        assert(not_lr0_grammar.parse_sequence("input/seq.txt") == None)
