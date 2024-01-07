from grammar import Grammar
from ParserOutput import ParserOutput

def print_menu():
    print(
        "---------------------------------------------\n"
        "1. Print set of non-terminals\n"
        "2. Print set of terminals\n"
        "3. Print set of productions\n"
        "4. Print productions for a given non-terminal\n"
        "5. CFG check\n"
        "6. Parse seq.txt\n"
        "7. Parse PIF.out\n"
        "0. Exit"
    )

def main():
    grammar = Grammar()
    grammar.read_grammar_from_file("input/G1.txt")

    while True:
        print_menu()
        option = input("Enter your option: ")
        if option == "1":
            print(str(grammar.non_terminals))
        elif option == "2":
            print(str(grammar.terminals))
        elif option == "3":
            print(str(grammar.productions))
        elif option == "4":
            non_terminal = input("Enter the non-terminal: ")
            print(str(grammar.productions_for_a_given_non_terminal(non_terminal)))
        elif option == "5":
            print(grammar.cfg_check())
        elif option == "6":
            grammar = Grammar()
            grammar.read_grammar_from_file("input/G1.txt")
            parser_output = ParserOutput(grammar)
            output_band = grammar.parse_sequence("input/seq.txt")
            if output_band is not None:
                parser_output.generateOutputTree(grammar.parse_sequence("input/seq.txt"))
                parser_output.PrintToFile(filePath="output/out1.txt")
                print("The result of parsing was written to output/out1.txt")
        elif option == "7":
            grammar = Grammar()
            grammar.read_grammar_from_file("input/G2_gabarsolon.txt")
            parser_output = ParserOutput(grammar)
            output_band = grammar.parse_sequence("input/PIF.out")
            if output_band is not None:
                parser_output.generateOutputTree()
                parser_output.PrintToFile(filePath="output/out2.txt")
                print("The result of parsing was written to output/out2.txt")
        elif option == "0":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
