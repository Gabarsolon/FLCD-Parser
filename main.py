from grammar import Grammar


def main():
    grammar = Grammar()
    grammar.read_grammar_from_file("G1.txt")
    print(grammar.cfg_check())

if __name__ == "__main__":
    main()