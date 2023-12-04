import unittest

from analysis_element import AnalysisElement
from grammar import Grammar
from production import Production


class TestLR0(unittest.TestCase):
    def setUp(self) -> None:
        self.longMessage = True
        self.grammar = Grammar()
        self.grammar.read_grammar_from_file("G1.txt")

    def tearDown(self) -> None:
        pass

    def test_closure(self):
        assert(self.grammar.closure([AnalysisElement(Production("S", ["a", "A"]), 1)])) == [
            AnalysisElement(Production("S", ["a", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]),      0)]

    def test_goto(self):
        analysis_element_set_to_test = [
            AnalysisElement(Production("S", ["a", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]),      0)
        ]

        assert(self.grammar.goto(analysis_element_set_to_test, "b") == [
            AnalysisElement(Production("A", ["b", "A"]), 1),
            AnalysisElement(Production("A", ["b", "A"]), 0),
            AnalysisElement(Production("A", ["c"]),      0)
        ])

    def test_col_can(self):
        assert(self.grammar.canonicalCollection() == [
            #s0
            [
                AnalysisElement(Production("S'", ["S"]),      0),
                AnalysisElement(Production("S",  ["a", "A"]), 0)
            ],
            #s1
            [
               AnalysisElement(Production("S'", ["S"]), 1)
            ],
            #s2
            [
                AnalysisElement(Production("S", ["a", "A"]), 1),
                AnalysisElement(Production("A", ["b", "A"]), 0),
                AnalysisElement(Production("A", ["c"]),     0)
            ],
            #s3
            [
                AnalysisElement(Production("S", ["a", "A"]), 2)
            ],
            #s4
            [
                AnalysisElement(Production("A", ["b", "A"]), 1),
                AnalysisElement(Production("A", ["b", "A"]), 0),
                AnalysisElement(Production("A", ["c"]),      0)
            ],
            #s5
            [
               AnalysisElement(Production("A", ["c"]), 1),
            ],
            #s6
            [
                AnalysisElement(Production("A", ["b", "A"]), 2)
            ]
        ])
