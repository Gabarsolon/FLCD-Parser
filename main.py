from analysis_element import AnalysisElement
from grammar import Grammar
from production import Production


def print_menu():
    print("1. Print set of non-terminals\n2. Print set of terminals\n3. Print set of productions\n"
          "4. Print productions for a given non-terminal\n5. CFG check\n6. Exit")


def main():
    grammar = Grammar()
    grammar.read_grammar_from_file("G1.txt")
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
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
